use std::collections::HashMap;

use crate::*;

use nox_ecs::Compiled;
use pyo3_polars::{PyDataFrame, PySeries};

#[pyclass]
pub struct Exec {
    pub exec: nox_ecs::WorldExec<Compiled>,
}

#[pymethods]
impl Exec {
    #[pyo3(signature = (ticks=1))]
    pub fn run(&mut self, ticks: usize) -> Result<(), Error> {
        for _ in 0..ticks {
            self.exec.run()?;
        }
        Ok(())
    }

    pub fn profile(&self) -> HashMap<&'static str, f64> {
        self.exec.profile()
    }

    pub fn history(&self) -> Result<PyDataFrame, Error> {
        let polars_world = self.exec.polars()?;
        let df = polars_world.join_archetypes()?;
        Ok(PyDataFrame(df))
    }

    fn column_array(&self, name: String) -> Result<PySeries, Error> {
        let id = ComponentId::new(&name);
        let series = self
            .exec
            .column_by_id(id)
            .ok_or(nox_ecs::Error::ComponentNotFound)?
            .series()?;
        Ok(PySeries(series))
    }
}
