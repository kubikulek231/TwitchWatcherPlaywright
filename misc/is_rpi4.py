import platform


class IsARM:
    @staticmethod
    def is_arm():
        return platform.machine() == 'aarch64'
