import jax
from typing import Any, Optional, Union
import numpy

class Entity: ...
class PrimitiveType:
    F64: PrimitiveType

class ComponentType:
    ty: PrimitiveType
    shape: jax.typing.ArrayLike
    U64: ClassVar[ComponentType]
    F64: ClassVar[ComponentType]
    F32: ClassVar[ComponentType]
    Edge: ClassVar[ComponentType]
    Quaternion: ClassVar[ComponentType]
    SpatialPosF64: ClassVar[ComponentType]
    SpatialMotionF64: ClassVar[ComponentType]

class ComponentId:
    def __init__(self, id: Union[int, str]): ...
class PipelineBuilder:
    def init_var(self, id: ComponentId, ty: ComponentType): ...
    def var_arrays(self) -> list[jax.typing.ArrayLike]: ...
class WorldBuilder:
    def spawn(self, archetype: Archetype) -> Entity: ...
    def spawn_with_entity_id(self, id: EntityId, archetype: Archetype) -> Entity: ...
    def insert_asset(self, asset: Any): ...
    def run(self, sys: System, time_step: Optional[float] = None, client: Optional[Client] = None): ...
    def build(self, sys: System, time_step: Optional[float] = None) -> Exec: ...
class EntityId:
    def __init__(self, id: int): ...
class Client:
    @staticmethod
    def cpu() -> Client: ...
class SpatialTransform:
    shape: jax.typing.ArrayLike
    def __init__(self, arr: jax.typing.ArrayLike): ...
    @staticmethod
    def from_linear(self, linear: jax.typing.ArrayLike) -> SpatialTransform: ...
    @staticmethod
    def from_angular(self, linear: jax.typing.ArrayLike) -> SpatialTransform: ...
    @staticmethod
    def from_axis_angle(self, axis: jax.typing.ArrayLike, angle: jax.typing.ArrayLike) -> SpatialTransform: ...
    def flatten(self) -> Any: ...
    @staticmethod
    def unflatten(aux: Any, jax : Any) -> Any: ...
    @staticmethod
    def from_array(arr: jax.typing.ArrayLike) -> SpatialTransform: ...
    @staticmethod
    def zero() -> SpatialTransform: ...
    def linear(self) -> jax.typing.ArrayLike: ...
    def angular(self) -> jax.typing.ArrayLike: ...
    def asarray(self) -> jax.typing.ArrayLike: ...

class SpatialForce:
    shape: jax.typing.ArrayLike
    def __init__(self, arr: jax.typing.ArrayLike): ...
    @staticmethod
    def from_array(arr: jax.typing.ArrayLike) -> SpatialForce: ...
    def flatten(self) -> Any: ...
    @staticmethod
    def unflatten(aux: Any, jax : Any) -> Any: ...
    def asarray(self) -> jax.typing.ArrayLike: ...
    @staticmethod
    def zero() -> SpatialForce: ...
    @staticmethod
    def from_linear(self, linear: jax.typing.ArrayLike) -> SpatialForce: ...
    @staticmethod
    def from_torque(self, linear: jax.typing.ArrayLike) -> SpatialForce: ...
    def force(self) -> jax.typing.ArrayLike: ...
    def torque(self) -> jax.typing.ArrayLike: ...
class SpatialMotion:
    shape: jax.typing.ArrayLike
    def __init__(self, arr: jax.typing.ArrayLike): ...
    @staticmethod
    def from_array(arr: jax.typing.ArrayLike) -> SpatialMotion: ...
    def flatten(self) -> Any: ...
    @staticmethod
    def unflatten(aux: Any, jax : Any) -> Any: ...
    def asarray(self) -> jax.typing.ArrayLike: ...
    @staticmethod
    def zero() -> SpatialMotion: ...
    @staticmethod
    def from_linear(self, linear: jax.typing.ArrayLike) -> SpatialMotion: ...
    @staticmethod
    def from_angular(self, linear: jax.typing.ArrayLike) -> SpatialMotion: ...
    def linear(self) -> jax.typing.ArrayLike: ...
    def angular(self) -> jax.typing.ArrayLike: ...
class SpatialInertia:
    shape: jax.typing.ArrayLike
    def __init__(self, arr: jax.typing.ArrayLike): ...
    @staticmethod
    def from_array(arr: jax.typing.ArrayLike) -> SpatialInertia: ...
    def flatten(self) -> Any: ...
    @staticmethod
    def unflatten(aux: Any, jax : Any) -> Any: ...
    @staticmethod
    def zero() -> SpatialInertia: ...
    @staticmethod
    def from_mass(self, mass: jax.typing.ArrayLike, com: jax.typing.ArrayLike, inertia: jax.typing.ArrayLike) -> SpatialInertia: ...
    def mass(self) -> jax.typing.ArrayLike: ...
class Quaternion:
    shape: jax.typing.ArrayLike
    def __init__(self, arr: jax.typing.ArrayLike): ...
    @staticmethod
    def from_array(arr: jax.typing.ArrayLike) -> Quaternion: ...
    def flatten(self) -> Any: ...
    @staticmethod
    def unflatten(aux: Any, jax : Any) -> Any: ...
    def asarray(self) -> jax.typing.ArrayLike: ...
    @staticmethod
    def zero() -> Quaternion: ...
    @staticmethod
    def from_axis_angle(self, axis: jax.typing.ArrayLike, angle: jax.typing.ArrayLike) -> Quaternion: ...
class RustSystem: ...
class Mesh:
    @staticmethod
    def cuboid(x: float, y: float, z: float) -> Mesh: ...
    @staticmethod
    def sphere(radius: float) -> Mesh: ...
    def bytes(self) -> bytes: ...
class Material:
    def bytes(self) -> bytes: ...
    @staticmethod
    def color(r: float, g: float, b: float) -> Material: ...
class Texture: ...
class Handle:
    def flatten(self) -> Any: ...
    @staticmethod
    def unflatten(aux: Any, jax : Any) -> Any: ...
class Pbr:
    def __init__(self, mesh: Mesh, material: Material): ...
    @staticmethod
    def from_url(url: str) -> Pbr: ...
    @staticmethod
    def from_path(path: str) -> Pbr: ...
    def bytes(self) -> bytes: ...
class EntityMetadata:
    def __init__(self, name: str, color: Optional[Color] = None): ...
    def asset_id(self) -> int: ...
    def bytes(self) -> bytes: ...
class Metadata: ...
class QueryInner: ...
class GraphQueryInner: ...
class Edge:
    def __init__(self, a: EntityId, b: EntityId): ...
    def flatten(self) -> Any: ...
    @staticmethod
    def unflatten(aux: Any, jax : Any) -> Any: ...
class ComponentData:
    id: ComponentId
    ty: ComponentType
    asset: bool
    from_expr: Callable[[Any], Any]
    name: Optional[str]
    def __init__(self, id: ComponentId, ty: ComponentType, asset: bool, from_expr: Callable[[Any], Any], name: Optional[str]): ...
    def to_metadata(self) -> Metadata: ...

class Conduit:
    @staticmethod
    def tcp(addr: str) -> Conduit: ...
class Exec:
    def run(self, client: Client): ...
    def column_array(self, id: ComponentId) -> numpy.ndarray: ...
class Color: ...
