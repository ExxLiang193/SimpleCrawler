import glob
import shutil
from typing import List

import instaloader
from PIL import Image


class InstagramImageSearcher:
    def __init__(self) -> None:
        self.loader = instaloader.Instaloader()

    def get_images_from_profile_posts(self, handle: str, limit: int = 5) -> List[Image.Image]:
        try:
            profile = instaloader.Profile.from_username(self.loader.context, handle)
        except Exception:
            # If the IG profile does not exist, return 0 images
            return list()

        posts = profile.get_posts()

        results = list()
        for i, post in enumerate(posts):
            dir_name = f"{profile.username}_{i}"
            # Post content is downloaded in base directory of project
            self.loader.download_post(post, dir_name)
            for jpg in glob.glob(f"{dir_name}/*.jpg"):
                if len(results) >= limit:
                    break
                results.append(Image.open(jpg).convert("RGB"))
            if len(results) >= limit:
                break

        # Cleanup the downloaded posts
        for dir_name in glob.glob(f"{profile.username}_*"):
            shutil.rmtree(dir_name)

        return results
