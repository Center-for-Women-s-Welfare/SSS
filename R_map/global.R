#setwd('C:/Users/cheng/OneDrive/Docuemnts/GitHub/SICSS/map')
#source('clean_location_data.R')
load("state_per.RData")
load("puma_per.RData")
load("comb_puma_mapinfor.RData")

comb_puma_mapinfor <- comb_puma_mapinfor%>%filter(fam_type %in% c("a1i0p0s0t0", "a2i0p0s0t0", "a2i1p0s0t0", "a2i0p1s0t0", "a2i0p0s1t0"))
