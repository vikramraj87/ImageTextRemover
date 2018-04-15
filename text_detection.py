from kv import Size, Rectangle
from kv.image import GrayscaleImage, Image, ImageMode
from kv.mser import MSERRegion, MSERDetector
from operator import attrgetter
import numpy as np
import cv2


class TextDetection:
    def __init__(self,
                 mser_delta: int=25,
                 threshold_delta_x: float=1.8,
                 threshold_delta_y: float=1.0,
                 threshold_num_groups: int=2,
                 num_dilations:int=0,
                 inpaint_radius:int=10):
        # Value for MSER Delta
        self._mser = MSERDetector(delta=mser_delta)

        # Value defining the minimum distance between horizontal groups
        self._threshold_delta_x = threshold_delta_x

        # Value defining the minimum distance between vertical groups
        self._threshold_delta_y = threshold_delta_y

        # Value defining the minimum number of regions in a group
        self._threshold_num_groups = threshold_num_groups

        # Number of dilations to apply to mask
        self._num_dilations = num_dilations

        # Inpaint radius
        self._inpaint_radius = inpaint_radius

    def detect(self, image: Image) -> (Image, GrayscaleImage):
        image_copy = Image.copy(image, target_mode=ImageMode.RGB)
        regions = self._mser.detect(image_copy)
        combined_regions = self._combine_enclosing_regions(regions)
        grouped_regions = self._group_mser_regions(combined_regions,
                                                   threshold_delta_x= self._threshold_delta_x,
                                                   threshold_delta_y=self._threshold_delta_y)
        flattened_groups = self._flatten_and_filter(grouped_regions,
                                                    threshold_num_groups=self._threshold_num_groups)
        mask = self._mask_from_groups(flattened_groups, image_copy.size)
        mask.dilate(iterations=self._num_dilations)
        inpainted_data = cv2.inpaint(image_copy.data,
                                     mask.data,
                                     self._inpaint_radius,
                                     cv2.INPAINT_NS)
        inpainted_image = Image(inpainted_data, mode=image_copy.mode)
        return inpainted_image, mask


    @staticmethod
    def _combine_enclosing_regions(regions: [MSERRegion]) -> [MSERRegion]:
        sort_key = attrgetter('bounding_box.origin.y', 'bounding_box.origin.x')
        sorted_regions = sorted(regions, key=sort_key)

        for i in range(len(sorted_regions) - 1):
            if not sorted_regions[i]:
                continue
            for j in range(i + 1, len(sorted_regions)):
                if not sorted_regions[j]:
                    continue
                reg1_bbox: Rectangle = sorted_regions[i].bounding_box
                reg2_bbox: Rectangle = sorted_regions[j].bounding_box
                if reg1_bbox.encloses(reg2_bbox):
                    sorted_regions[i].add_region(sorted_regions[j])
                    sorted_regions[j] = None

        return [region for region in sorted_regions if region]

    @staticmethod
    def _group_mser_regions(regions: [MSERRegion],
                           threshold_delta_x: float = 1.8,
                           threshold_delta_y: float = 1.0) -> [[[MSERRegion]]]:
        # Initially sort regions by baseline
        v_sorted_regions: [MSERRegion] = sorted(regions, key=attrgetter('bounding_box.end.y'))

        # Group vertically nearby areas
        v_groups: [[MSERRegion]] = [[]]
        for v_sorted_region in v_sorted_regions:
            # Add initial region and do nothing
            if len(v_groups[-1]) == 0:
                v_groups[-1].append(v_sorted_region)
                continue

            v_group_first_region = v_groups[-1][0]
            delta_y = abs(
                v_group_first_region.bounding_box.end.y - v_sorted_region.bounding_box.end.y
            )
            median_height = np.median(
                [region.bounding_box.size.height for region in v_groups[-1]]
            )
            norm_delta_y = delta_y / median_height
            if norm_delta_y > threshold_delta_y:
                v_groups.append([v_sorted_region])
                continue

            v_groups[-1].append(v_sorted_region)

        total_regions_in_vertical_groups = sum([len(v_group) for v_group in v_groups])
        assert (len(regions) == total_regions_in_vertical_groups)

        # Group each vertical group into horizontal groups
        groups: [[[MSERRegion]]] = []
        for v_group in v_groups:
            groups.append([[]])
            median_width = np.median(
                [region.bounding_box.size.width for region in v_group]
            )
            h_sorted_regions: [MSERRegion] = sorted(v_group,
                                                    key=attrgetter('bounding_box.origin.x'))
            for h_sorted_region in h_sorted_regions:
                if len(groups[-1][-1]) == 0:
                    groups[-1][-1].append(h_sorted_region)
                    continue

                h_prev_region = groups[-1][-1][-1]
                delta_x = abs(
                    h_prev_region.bounding_box.origin.x - h_sorted_region.bounding_box.origin.x
                )
                norm_delta_x = delta_x / median_width
                if norm_delta_x > threshold_delta_x:
                    groups[-1].append([h_sorted_region])
                    continue

                groups[-1][-1].append(h_sorted_region)

        total_regions_in_groups = 0
        for v_grp in groups:
            for h_grp in v_grp:
                total_regions_in_groups += len(h_grp)
        assert (len(regions) == total_regions_in_groups)

        return groups

    @staticmethod
    def _flatten_and_filter(groups: [[[MSERRegion]]], threshold_num_groups: int = 2) -> [[MSERRegion]]:
        filtered_groups: [[MSERRegion]] = []
        for v_group in groups:
            for h_group in v_group:
                if len(h_group) > threshold_num_groups:
                    filtered_groups.append(h_group)
        return filtered_groups

    @staticmethod
    def _mask_from_groups(groups: [[MSERRegion]], size: Size) -> GrayscaleImage:
        regions = []
        for group in groups:
            regions += group
        return __class__._mask_from_mser_regions(regions, size)


    @staticmethod
    def _mask_from_mser_regions(regions: [MSERRegion], size: Size) -> GrayscaleImage:
        mask = GrayscaleImage.black_canvas(size)
        for region in regions:
            region.plot_in_mask(mask)
        return mask


# def rectangle_for_regions(regions: [MSERRegion]):
#     rect = None
#     for region in regions:
#         if rect is None:
#             rect = region.bounding_box
#             continue
#         rect = Rectangle.enclosing_rectangle(rect, region.bounding_box)
#     return rect






