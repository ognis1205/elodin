#![no_main]
#![no_std]

extern crate alloc;

use alloc::boxed::Box;
use cortex_m::delay::Delay;
use embedded_hal_compat::ForwardCompat;
use fugit::{ExtU32 as _, RateExtU32 as _};
use hal::{i2c, pac, usart};

use roci_multicopter::bsp::aleph as bsp;
use roci_multicopter::{
    bmm350, crsf, dma::*, dshot, healing_usart, i2c_dma::*, led, monotonic, peripheral::*,
};

const ELRS_RATE: fugit::Hertz<u64> = fugit::Hertz::<u64>::Hz(8000);
const ELRS_PERIOD: fugit::MicrosDuration<u64> = ELRS_RATE.into_duration();

#[cortex_m_rt::entry]
fn main() -> ! {
    defmt::info!("Starting");
    roci_multicopter::init_heap();

    let cp = cortex_m::Peripherals::take().unwrap();
    let mut dp = pac::Peripherals::take().unwrap();
    let pins = bsp::Pins::take().unwrap();
    let bsp::Pins { pd10: led_sg0, .. } = pins;
    defmt::info!("Configured peripherals");

    let clock_cfg = bsp::clock_cfg(dp.PWR);
    clock_cfg.setup().unwrap();
    let mut delay = Delay::new(cp.SYST, clock_cfg.systick()).forward();
    defmt::info!("Configured clocks");

    let mut monotonic = monotonic::Monotonic::new(dp.TIM2, &clock_cfg);
    defmt::info!("Configured monotonic timer");

    let mut running_led = led::PeriodicLed::new(led_sg0, 100u32.millis());

    let elrs_uart = Box::new(healing_usart::HealingUsart::new(usart::Usart::new(
        dp.USART3,
        crsf::CRSF_BAUDRATE,
        usart::UsartConfig::default(),
        &clock_cfg,
    )));
    defmt::info!("Configured ELRS UART");
    let mut crsf = crsf::CrsfReceiver::new(elrs_uart);

    // Generate a 600kHz PWM signal on TIM3
    let pwm_timer = dp.TIM3.timer(600.kHz(), Default::default(), &clock_cfg);
    defmt::info!("Configured PWM timer");

    let [i2c1_rx, dshot_tx, ..] = dp.DMA1.split();

    defmt::debug!("Initializing I2C + DMA");
    let mut i2c1_dma = I2cDma::new(
        dp.I2C1,
        i2c::I2cConfig {
            speed: i2c::I2cSpeed::FastPlus1M,
            ..Default::default()
        },
        i2c1_rx,
        &clock_cfg,
        &mut dp.DMAMUX1,
        &mut dp.DMAMUX2,
    );
    let mut bmm350 = bmm350::Bmm350::new(&mut i2c1_dma, bmm350::Address::Low, &mut delay).unwrap();

    let mut dshot_driver = dshot::Driver::new(pwm_timer, dshot_tx, &mut dp.DMAMUX1);

    let mut last_elrs_update = monotonic.now();
    let mut last_dshot_update = monotonic.now();

    loop {
        let now = monotonic.now();
        let ts = now.duration_since_epoch();

        if now.checked_duration_since(last_elrs_update).unwrap() > ELRS_PERIOD {
            last_elrs_update = now;
            defmt::trace!("{}: Reading ELRS data", ts);

            crsf.update(monotonic.now());
        } else if now.checked_duration_since(last_dshot_update).unwrap() > dshot::UPDATE_PERIOD {
            last_dshot_update = now;
            defmt::trace!("{}: Sending DSHOT data", ts);

            let control = crsf.frsky();
            let armed = control.armed();
            dshot_driver.write_throttle([control.throttle.into(); 4], armed, now);
        }

        let mag_updated = bmm350.update(&mut i2c1_dma);
        running_led.update(now);

        if mag_updated && bmm350.data.sample % 400 == 0 {
            defmt::info!(
                "{}: BMM350 sample {}: {}",
                ts,
                bmm350.data.sample,
                bmm350.data
            );
        }
    }
}
