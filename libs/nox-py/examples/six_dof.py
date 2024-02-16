import elodin
import jax
import jax.numpy as np
from elodin import Component, ComponentType, system, ComponentArray, Archetype, WorldBuilder, Client, ComponentId, Query, WorldPos, WorldAccel, WorldVel, Inertia, Force, Body, six_dof, Material, Mesh

w = WorldBuilder()
b = Body(
    world_pos = WorldPos.from_linear(np.array([0.,0.,0.])),
    world_vel = WorldVel.from_linear(np.array([1.,0.,0.])),
    world_accel = WorldVel.from_linear(np.array([0.,0.,0.])),
    force = Force.zero(),
    inertia = Inertia.from_mass(1.0),
    mesh = w.insert_asset(Mesh.cuboid(1.0, 1.0, 1.0)),
    material = w.insert_asset(Material.color(1.0, 1.0, 1.0))
)
w.spawn(b)
client = Client.cpu()
exec = w.run(client, six_dof(1.0 / 60.0))
