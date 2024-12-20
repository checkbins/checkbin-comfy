import checkbin


class CheckbinStartRunNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "token": ("STRING",),
            },
            "optional": {
                "app_key": ("STRING",),
                "checkin_id": ("STRING",),
                "set_id": ("STRING",),
                "run_id": ("STRING",),
                "sample_size": ("INT",),
            },
        }

    @classmethod
    def IS_CHANGED(cls):
        return float("NaN")

    RETURN_TYPES = ("CHECKBIN",)
    RETURN_NAMES = ("bin",)
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "tracing"
    FUNCTION = "start_run"

    def start_run(
        self,
        token,
        app_key="comfyui",
        checkin_id=None,
        set_id=None,
        run_id=None,
        sample_size=None,
    ):
        checkbin.authenticate(token=token)
        checkbin_app = checkbin.App(app_key=app_key)

        if checkin_id == "":
            checkin_id = None
        if set_id == "":
            set_id = None
        if run_id == "":
            run_id = None
        if sample_size == 0:
            sample_size = None

        with checkbin_app.start_run(
            checkin_id=checkin_id,
            set_id=set_id,
            run_id=run_id,
            sample_size=sample_size,
        ) as bins:
            return (list(bins),)
