import checkbin
import os


class CheckbinStartRunNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "token": ("STRING",),
            },
            "optional": {
                "app_key": ("STRING",),
                "directory": ("STRING",),
                "checkin_id": ("STRING",),
                "set_id": ("STRING",),
                "run_id": ("STRING",),
                "sample_size": ("INT",),
            },
        }

    @classmethod
    def IS_CHANGED(cls, **kwargs):
        return float("NaN")

    RETURN_TYPES = ("CHECKBIN",)
    RETURN_NAMES = ("bin",)
    OUTPUT_IS_LIST = (True,)
    CATEGORY = "comparison"
    FUNCTION = "start_run"

    def start_run(
        self,
        token,
        app_key="comfyui",
        directory=None,
        checkin_id=None,
        set_id=None,
        run_id=None,
        sample_size=None,
    ):
        checkbin.authenticate(token=token)
        checkbin_app = checkbin.App(app_key=app_key)

        if directory is not None and directory != "":
            if not os.path.isdir(directory):
                raise FileNotFoundError(f"Directory '{directory} cannot be found.'")
            dir_files = os.listdir(directory)
            if len(dir_files) == 0:
                raise FileNotFoundError(f"No files in directory '{directory}'.")

            # Filter files by extension
            valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
            dir_files = [
                f
                for f in dir_files
                if any(f.lower().endswith(ext) for ext in valid_extensions)
            ]

            input_set = checkbin_app.create_input_set(
                "ComfyUI auto generated input set"
            )

            for file in dir_files:
                checkin = input_set.add_input()
                checkin.upload_file("image", f"{directory}/{file}", "image")

            set_id = input_set.submit()

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
