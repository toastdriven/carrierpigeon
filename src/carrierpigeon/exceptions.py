class CarrierPigeonError(Exception):
    pass


class CarrierLost(CarrierPigeonError):
    pass


class ValidationError(CarrierPigeonError):
    errors = []

    def __init__(self, errors):
        self.errors = errors
        readable = ", ".join([f"'{err_info[0]}: {err_info[1]}" for err_info in self.errors])
        self.message = f"Message validation failed: {readable}"
