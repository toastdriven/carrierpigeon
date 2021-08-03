class CarrierPigeonError(Exception):
    pass


class CarrierLost(CarrierPigeonError):
    pass


class ValidationError(CarrierPigeonError):
    errors = []
