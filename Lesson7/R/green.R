# Rodrigo Almeida, Ping
# Team Dragon Masters
# 17/01/2017

# Greenest regions(municipality/provinces)
green_data <- function(r_stack, regions){
  r_masked <- mask(r_stack, regions)
  green_index <- extract(r_masked, regions, fun = mean,df=T )
  # Add NDVI value to data frame
  result <- cbind(regions@data, green_index)
  # Only calculate columns from January to December,negative sign means negelect those columns
  index_Before_January <- (grep("January", colnames(result)) - 1)
  result$year <- rowMeans(result[-1:(-index_Before_January)], na.rm = T)
  return(result)
}

# Find out the greenest district
green_district <- function(dataframe, period){
  id <- which.max(dataframe[[period]])
  # Use if condition to accept both municipality and province administrative as input
  if ('NAME_2' %in% colnames(dataframe)) {
    return(dataframe[id,]$NAME_2)
    
  } else {
    return(dataframe[id,]$NAME_1)
    
  }
}