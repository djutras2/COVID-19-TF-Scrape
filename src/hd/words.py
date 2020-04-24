'''Various word collections for use in scraping state hd websites'''

# words that will cause a URL to be skipped
stop_words = ["facebook", "ethics", "policy", "symptoms", "flyer", "eviction", "signage", "guidance", "unemployment", "school", "disabilit", "financial", "you", "homemade", "yourself", "cdc.gov", "masks", "whitehouse.gov", "cloth", "face", "faq", "education", "recommendations", "emotional", "videos", "providers"]

# words that will cause a PDF, CSV, etc. to saves
search_words = ["locality", "jurisdiction", "counts", "data", "map", "update", "daily", "zip_code", "zip-code", "zipcode", "code", "numbers", "analysis"]

# words that will cause a URL to be saves as a potential WMS
wms_words = ["tableau", "mapbox", "arcgis", "esri", "leaflet", "openstreetmap", "openlayers", "cartodb"]

# list of all states (and DC)
states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado",
  "Connecticut","Delaware","District of Columbia", "Florida","Georgia","Hawaii","Idaho","Illinois",
  "Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland",
  "Massachusetts","Michigan","Minnesota","Mississippi","Missouri","Montana",
  "Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York",
  "North Carolina","North Dakota","Ohio","Oklahoma","Oregon","Pennsylvania",
  "Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
  "Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]