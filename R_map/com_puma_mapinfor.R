library(readr)
library(tidyverse)
setwd("~/Downloads/sss")
comb_puma_housea <- read_csv("comb_puma_housea.csv",col_types = cols(ST = col_character()))
comb_puma_houseb <- read_csv("comb_puma_houseb.csv",col_types = cols(ST = col_character()))
comb_puma_housec <- read_csv("comb_puma_housec.csv",col_types = cols(ST = col_character()))
comb_puma_housed <- read_csv("comb_puma_housed.csv",col_types = cols(ST = col_character()))

map_pumainfor <- function(df) {
  df_g <- df %>% drop_na(state)%>%group_by(PUMA,fam_type,ST,state)%>%
    summarise(median_sss=median(sss_weight), median_poverty=median(poverty_th))
  df_g$percent <- round((df_g$median_sss-df_g$median_poverty)/df_g$median_poverty*100,2)
  return(df_g)
}
comb_puma_housea_g <- map_pumainfor(comb_puma_housea)
comb_puma_houseb_g <- map_pumainfor(comb_puma_houseb)
comb_puma_housec_g <- map_pumainfor(comb_puma_housec)
comb_puma_housed_g <- map_pumainfor(comb_puma_housed)
comb_puma_mapinfor = do.call("rbind", list(comb_puma_housea_g, comb_puma_houseb_g, comb_puma_housec_g,comb_puma_housed_g))
save(comb_puma_mapinfor, file = "comb_puma_mapinfor.RData")


comb_puma_housea_g%>%group_by(PUMA,fam_type) %>%count()
