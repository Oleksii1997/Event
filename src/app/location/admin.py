from sqladmin import ModelView
from src.app.location.models import AreaModel, RegionModel, CommunityModel, CityModel


class AreaModelAdmin(ModelView, model=AreaModel):
    """Реєструємо модель областей в адмінпанелі"""

    name = "Area"
    name_plural = "Area"
    icon = "fa-solid fa-location-dot"
    category = "Location"
    page_size = 50
    page_size_options = [25, 50, 100]
    column_details_list = [AreaModel.id, AreaModel.area_name]
    column_sortable_list = [AreaModel.area_name]
    column_list = [AreaModel.id, AreaModel.area_name]
    column_labels = {AreaModel.id: "Area ID", AreaModel.area_name: "Area name"}
    column_searchable_list = [AreaModel.id, AreaModel.area_name]
    column_export_list = ["id", "area_name"]
    form_edit_rules = ["id", "area_name"]


class RegionModelAdmin(ModelView, model=RegionModel):
    """Реєстрація моделей районів в адмінпанелі"""

    name = "Region"
    name_plural = "Regions"
    icon = "fa-solid fa-earth-europe"
    category = "Location"
    page_size = 50
    page_size_options = [25, 50, 100, 1000]
    column_sortable_list = [RegionModel.region_name]
    column_details_list = [
        RegionModel.id,
        RegionModel.region_name,
        RegionModel.region_area,
    ]
    column_list = [
        RegionModel.id,
        RegionModel.region_name,
    ]
    column_labels = {
        RegionModel.id: "Region ID",
        RegionModel.region_name: "Region name",
    }
    column_searchable_list = [RegionModel.id, RegionModel.region_name]
    column_export_list = ["id", "region_name", "area_id", "region_area"]
    form_edit_rules = ["id", "region_name", "area_id", "region_area"]


class CommunityModelAdmin(ModelView, model=CommunityModel):
    """Реєстрація моделі громад в адмінпанелі"""

    name = "Community"
    name_plural = "Community"
    icon = "fa-solid fa-mountain-city"
    category = "Location"
    page_size = 50
    page_size_options = [25, 50, 100, 1000]
    column_sortable_list = [CommunityModel.community_name]
    column_details_list = [
        CommunityModel.id,
        CommunityModel.community_name,
        CommunityModel.community_region,
    ]
    column_list = [
        CommunityModel.id,
        CommunityModel.community_name,
    ]
    column_labels = {
        CommunityModel.id: "Community ID",
        CommunityModel.community_name: "Community name",
    }
    column_searchable_list = [CommunityModel.id, CommunityModel.community_name]
    column_export_list = "__all__"
    form_edit_rules = ["id", "community_name", "region_id", "community_region"]


class CityModelAdmin(ModelView, model=CityModel):
    """Реєстрація моделі населених пунктів в адмінпанелі"""

    name = "City"
    name_plural = "City"
    icon = "fa-solid fa-tree-city"
    category = "Location"
    page_size = 50
    page_size_options = [25, 50, 100, 1000]
    column_sortable_list = [CityModel.city_name]
    column_details_list = [CityModel.id, CityModel.city_name, CityModel.city_community]
    column_list = [
        CityModel.id,
        CityModel.city_name,
    ]
    form_columns = [CityModel.id, CityModel.city_name, CityModel.city_community]
    column_labels = {
        CityModel.id: "City ID",
        CityModel.city_name: "City name",
    }
    column_searchable_list = [CityModel.id, CityModel.city_name]
    column_export_list = "__all__"
    form_edit_rules = ["id", "city_name", "community_id", "city_community"]
