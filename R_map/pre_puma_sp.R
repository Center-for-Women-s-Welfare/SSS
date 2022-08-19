library(sf)
library(tidyverse)
library(readr)
setwd("~/Downloads/sss")
us_puma <- st_read("us_puma/us_pumas.shp")
state_sp <- st_read("cb_2018_us_state_500k/cb_2018_us_state_500k.shp")
state <- state_sp %>% select(STATEFP,NAME,STUSPS)
state$geometry <- NULL
us_puma <- us_puma%>%left_join(state,by = c('STATEFP10' = 'STATEFP'))
puma_pera <- read_csv("for_vis_pumaa.csv", 
                         col_types = cols(state_fips = col_character(), 
                                          puma_code = col_character()))
puma_perb <- read_csv("for_vis_pumab.csv", 
                     col_types = cols(state_fips = col_character(), 
                                      puma_code = col_character()))
puma_perc <- read_csv("for_vis_pumac.csv", 
                     col_types = cols(state_fips = col_character(), 
                                      puma_code = col_character()))
puma_perd <- read_csv("for_vis_pumad.csv", 
                     col_types = cols(state_fips = col_character(), 
                                      puma_code = col_character()))
puma_per = do.call("rbind", list(puma_pera, puma_perb, puma_perc,puma_perd))
puma_per <- puma_per %>%
  left_join(us_puma, by = c("state_fips" = "STATEFP10",'puma_code' = 'PUMACE10'))
st_geometry(puma_per) <- puma_per$geometry
puma_per$per_below_sss_puma <- round(puma_per$per_below_sss_puma*100,2)
puma_per$per_below_poverty_puma <- round(puma_per$per_below_poverty_puma*100,2)
puma_per <- st_transform(puma_per, crs = 4326)
names(puma_per)[names(puma_per) == 'GEOID10'] <- 'GEOID'
#names(puma_per)[names(puma_per) == 'per_below_sss'] <- 'per_below_sss_puma'
names(puma_per)[names(puma_per) == 'NAME'] <- 'STATE_NAME'
names(puma_per)[names(puma_per) == 'NAME10'] <- 'NAME'
save(puma_per, file = "puma_per.RData")
