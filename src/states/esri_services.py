from .state_helper import fetch_from_esri

def fetch_pa():
    location = "PA.csv"
    url = "https://services2.arcgis.com/xtuWQvb2YQnp0z3F/arcgis/rest/services/Zip_Code_COVID19_Case_Data/FeatureServer/0"

    fetch_from_esri(location, url, 'ZIP_CODE', 'Positive')

def fetch_nc():
    location = "NC.csv"
    url = "https://services.arcgis.com/iFBq2AW9XO0jYYF7/arcgis/rest/services/Covid19byZIPnew/FeatureServer/0"

    fetch_from_esri(location, url, 'ZIPCode', 'Cases', deaths_field="Deaths")

def fetch_az():
    location = "AZ.csv"
    url = "https://services1.arcgis.com/mpVYz37anSdrK4d8/arcgis/rest/services/CVD_ZIPS_FORWEBMAP/FeatureServer/0"

    fetch_from_esri(location, url, 'POSTCODE', 'ConfirmedCaseCount')