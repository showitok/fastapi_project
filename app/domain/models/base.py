from dataclasses import dataclass
from typing import ClassVar, Any, Self

from psygnal import EmissionInfo, SignalGroupDescriptor


@dataclass
class BaseModel:

    _events: ClassVar[SignalGroupDescriptor] = SignalGroupDescriptor()

    def __post_init__(self):
        self._events.connect(self._on_event)
        self._modified_fields = {}

    def _on_event(self, info: EmissionInfo):
        new_value, org_value = list(info.args)
        if new_value == org_value:
            return
        field_name = info.signal.name

        if field_name not in self._modified_fields:
            self._modified_fields[field_name] = {
                "org_value": org_value,
                "new_value": new_value,
            }
        else:
            self._modified_fields[field_name].update({
                "new_value": new_value,
            })

    def __setattr__(self, key: str, value: Any) -> None:
        if method := getattr(self, "validate_{}".format(key), None):
            value = method(value)
        super().__setattr__(key, value)

    @property
    def modified_fields(self) -> dict:
        return self._modified_fields

    def rollback(self) -> Self:
        for _field, _value in self._modified_fields.items():
            setattr(self, _field, _value["org_value"])

        self._modified_fields.clear()
        return self

