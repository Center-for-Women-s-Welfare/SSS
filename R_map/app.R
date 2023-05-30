##this is for shiny map


library(shinydashboard)     # Dashboard version of shiny
library(shinydashboardPlus) # Dashboard extras (mainly right sidebar)
library(shiny)              # Base shiny
library(shinyWidgets)       # For cool buttons, sliders, checkboxes, etc.
library(leaflet)            # For interactive maps
library(htmltools)          # Custom HTML control
library(RColorBrewer)       # Color palette management
library(shinycssloaders)    # For loading spinner/animation
library(shinyjs)            # For running custom Java Script code in Shiny evironment
library(shinyBS)          # For tooltips, popovers, etc.
library(tigris)
library(shinythemes)
library(readr)
library(sf)
library(gridExtra)
library(plotly)
library(stringr)
library(dplyr)
library(tidyverse)
library(classInt)
library(ggalt)



#load files in global
source('global.R')

#cat(ls(), "\n")
# Create a UI for the map
cat(file=stderr(), "done the preamble", "\n")
ui <- bootstrapPage(
  #tags$head(includeHTML("gtag.html")),
  navbarPage(theme = shinytheme("flatly"), collapsible = FALSE,
             "Center for Women’s Welfare (CWW)", id="nav",
             tabPanel("Self-Sufficiency Standard",
                      div(class="outer",
                          tags$head(includeCSS("style.css")),
                          leafletOutput("main_map", width="100%", height="100%"),
                          # the information pad on the top left
                          absolutePanel(id = "controls", class = "panel panel-default",
                                        top = 100, left = 55, width = 400, fixed=TRUE,
                                        draggable = TRUE, height = "auto",
                                        #img(src="logo.png",height=37,width=110,align = "left"),
                                        pickerInput("select_state", label = h3("State Selection"), inline = F,
                                                    selected = "No Selection",
                                                    choices = c('No Selection',sort(c(as.character(state_per$NAME)))),
                                                    choicesOpt = list(
                                                      style = rep(("color:black; font-size: 110%;"), 56)),
                                                    options = list(liveSearch = TRUE)),
                                        h4(textOutput("below_sss"), align = "left"),
                                        h4(textOutput("below_poverty"), align = "left")
                                        ),
                          # the information pad on the top right
                          absolutePanel(id = "controls", class = "panel panel-default",
                                        top = 100, right = 55, width = 600, fixed=TRUE,
                                        draggable = TRUE, height = "auto",
                                        span(h4(textOutput('puma_infor'), align = "left"), style="color:#01806f"),
                                        span(h5(textOutput('puma_name'), align = "left"), style="color:#01806f"),
                                        span(h5(textOutput('puma_sss'), align = "left"), style="color:#01806f"),
                                        span(h5(textOutput('puma_poverty'), align = "left"), style="color:#01806f"),
                                        h5(textOutput('fama1'), align = "left"),
                                        h5(textOutput('fama2'), align = "left"),
                                        h5(textOutput('fama2i1'), align = "left"),
                                        h5(textOutput('fama2p1'), align = "left"),
                                        h5(textOutput('fama2s1'), align = "left"),

                          ),
                          # the logo position on the bottom left
                          absolutePanel(id = "logo", class = "card", bottom = 20, left = 60, width = 160, fixed=TRUE, draggable = FALSE, height = "auto",
                                        tags$a(href='https://selfsufficiencystandard.org/', tags$img(src='cww.png',height='50',width='300')))

                          )
                      )
             )
  )



cat(file=stderr(), "Starting Server", "\n")

server <- function(input, output, session) {
  # Pre-define map function to be called later
  make_leaflet_map <- function() {
    #add base map
    map1 <- leaflet() %>%

      addProviderTiles("CartoDB.Positron", options = providerTileOptions(minZoom = 3), group = "Plain basemap") %>%
      addProviderTiles("CartoDB.Positron", options = providerTileOptions(minZoom = 3), group = "plain Map")  %>%
      addMapPane("Polygons", zIndex = 400) #%>%   # Pane z-Index for polygons to stay underneath the markers
      #

    return(map1)
  }
  # Rendering the main map
  output$main_map <- renderLeaflet({make_leaflet_map()
    })

  #update the dataset
  update_dataset <- reactive({
    if(input$select_state == 'No Selection'){
      data_set <-state_per
    }
    if(input$select_state != 'No Selection'){
      data_set <- puma_per %>% filter(STATE_NAME == input$select_state)
    }
    return(data_set)})

  #fill colors
  quantcolors <- reactive({
    # Color pallete for SSS
    if(input$select_state == 'No Selection'){
      return(colorBin(c('#7E76AA', '#4B2E83', '#27194D'), update_dataset()$per_below_sss, bins=3,pretty = TRUE))}
    if(input$select_state != 'No Selection'){
      return(colorBin("Purples", update_dataset()$per_below_sss_puma,bins=8 ,pretty = TRUE))}
    })


  #get the % of below sss when the a state were chosen
  output$below_sss <- renderText({
    if(input$select_state != 'No Selection'){
      st <- state_per%>%filter(NAME == input$select_state)
      per <- st$per_below_sss
      paste0(prettyNum(per,4, big.mark=","),'% Below Self Sufficiency Standard')
    }
    else if(!is.null(data_of_click$clickedGeography$id)){
      if(nchar(data_of_click$clickedGeography$id)==2){
        st <- state_per%>%filter(GEOID==data_of_click$clickedGeography$id)
        per <- st$per_below_sss
        paste0(prettyNum(per,4, big.mark=","),'% Below Self Sufficiency Standard')
      }
    else{
      paste0('')
    }}
  })

  #get the % of below poverty when the polygon were chosen
  output$below_poverty <- renderText({
    if(input$select_state != 'No Selection'){
      st <- state_per%>%filter(NAME == input$select_state)
      per <- st$per_below_poverty
      paste0(prettyNum(per,4,big.mark=","),'% Below Poverty Threshold')
    }
    else if(!is.null(data_of_click$clickedGeography$id)){
      if(nchar(data_of_click$clickedGeography$id)==2){
        st <- state_per%>%filter(GEOID==data_of_click$clickedGeography$id)
        per <- st$per_below_poverty
        paste0(prettyNum(per,4,big.mark=","),'% Below Poverty Threshold')
      }}
    else{
      paste0('')
    }
  })



#######################################################
  # set empty click container
  data_of_click <- reactiveValues(clickedMarker = NULL, clickedGeography = NULL)

  #### layer click ####
  # Geography click
  observeEvent(input$main_map_shape_click, {
    data_of_click$clickedGeography <- input$main_map_shape_click
    # if the polygon is county add county boundary
    if(nchar(data_of_click$clickedGeography$id)>3){
      leafletProxy("main_map") %>%
        addMapPane("puma", zIndex = 430) %>%
        clearGroup("puma") %>%
        addPolylines(data = puma_per %>% filter(GEOID==data_of_click$clickedGeography$id),
                     fill = FALSE,
                     weight = 5,
                     color = "black",
                     group = "puma")
    }
    # if the polygon is state add state boundary
    if(nchar(data_of_click$clickedGeography$id)==2){
      leafletProxy("main_map") %>%
        addMapPane("puma", zIndex = 430) %>%
        clearGroup("puma") %>%
        addPolylines(data = state_per %>% filter(GEOID==data_of_click$clickedGeography$id),
                     fill = FALSE,
                     weight = 5,
                     color = "black",
                     group = "puma")
    }


  })
  # return puma information for the upper right pad
  output$puma_infor <- renderText({
    if(!is.null(data_of_click$clickedGeography$id)){
      if(nchar(data_of_click$clickedGeography$id)>3){
        paste0('PUMA Information')
      }
      else{
        paste0("Click on a PUMA polygon to view details.")}}
    else{
      paste0("Click on a PUMA polygon to view details.")}

  })
  # return puma name for the upper right pad after clicking
  output$puma_name <- renderText({
    if(!is.null(data_of_click$clickedGeography$id)){
      if(nchar(data_of_click$clickedGeography$id)>3){
      data = puma_per %>% filter(GEOID==data_of_click$clickedGeography$id)
      puma_name <- data$NAME
      paste0('PUMA Name: ',puma_name)
      }
      else{
        paste0("")}
    }
    else{
      paste0("")}
  })
  # return puma sss % for the upper right pad after clicking
  output$puma_sss <- renderText({
    if(!is.null(data_of_click$clickedGeography$id)){
      if(nchar(data_of_click$clickedGeography$id)>3){
        data = puma_per %>% filter(GEOID==data_of_click$clickedGeography$id)
        puma_sss <- data$per_below_sss_puma
        paste0('PUMA Below SSS: ',puma_sss,'%')
      }
      else{
        paste0("")}
    }
    else{
      paste0("")}
  })

  # return puma poverty % for the top right pad after clicking
  output$puma_poverty <- renderText({
    if(!is.null(data_of_click$clickedGeography$id)){
      if(nchar(data_of_click$clickedGeography$id)>3){
        data = puma_per %>% filter(GEOID==data_of_click$clickedGeography$id)
        puma_poverty <- data$per_below_poverty_puma
        paste0('PUMA Below Poverty Threshold: ',puma_poverty,'%')
      }
      else{
        paste0("")}
    }
    else{
      paste0("")}
  })
  # return standard of 1 adult
  output$fama1 <- renderText({
    if(!is.null(data_of_click$clickedGeography$id)){
      if(nchar(data_of_click$clickedGeography$id)>3){
        puma = puma_per%>%filter(GEOID==data_of_click$clickedGeography$id)
        data = comb_puma_mapinfor %>% filter(PUMA==puma$puma_code & state==puma$states)
        fam <- data%>%filter(fam_type=='a1i0p0s0t0')
        paste0('1 Adult: Median SSS ',prettyNum(fam$median_sss,3,big.mark=","), '/Poverty ',prettyNum(fam$median_poverty,3,big.mark=","))
      }
      else{
        paste0("")}
    }
    else{
      paste0("")}
  })
  # return standard of 2 adults
  output$fama2 <- renderText({
    if(!is.null(data_of_click$clickedGeography$id)){
      if(nchar(data_of_click$clickedGeography$id)>3){
        puma = puma_per%>%filter(GEOID==data_of_click$clickedGeography$id)
        data = comb_puma_mapinfor %>% filter(PUMA==puma$puma_code & state==puma$states)
        fam <- data%>%filter(fam_type=='a2i0p0s0t0')
        paste0('2 Adults: Median SSS ',prettyNum(fam$median_sss,3,big.mark=","), '/Poverty ',prettyNum(fam$median_poverty,3,big.mark=","))
      }
      else{
        paste0("")}
    }
    else{
      paste0("")}
  })
  # return standard of 2 adults 1 infant
  output$fama2i1 <- renderText({
    if(!is.null(data_of_click$clickedGeography$id)){
      if(nchar(data_of_click$clickedGeography$id)>3){
        puma = puma_per%>%filter(GEOID==data_of_click$clickedGeography$id)
        data = comb_puma_mapinfor %>% filter(PUMA==puma$puma_code & state==puma$states)
        fam <- data%>%filter(fam_type=='a2i1p0s0t0')
        paste0('2 Adults & 1 Infant: Median SSS ',prettyNum(fam$median_sss,3,big.mark=","), '/Poverty ',prettyNum(fam$median_poverty,3,big.mark=","))
      }
      else{
        paste0("")}
    }
    else{
      paste0("")}
  })
  # return standard of 2 adults 1 preschooler
  output$fama2p1 <- renderText({
    if(!is.null(data_of_click$clickedGeography$id)){
      if(nchar(data_of_click$clickedGeography$id)>3){
        puma = puma_per%>%filter(GEOID==data_of_click$clickedGeography$id)
        data = comb_puma_mapinfor %>% filter(PUMA==puma$puma_code & state==puma$states)
        fam <- data%>%filter(fam_type=='a2i0p1s0t0')
        paste0('2 Adults & 1 Preschooler: Median SSS ',prettyNum(fam$median_sss,3,big.mark=","), '/Poverty ',prettyNum(fam$median_poverty,3,big.mark=","))
      }
      else{
        paste0("")}
    }
    else{
      paste0("")}
  })
  # return standard of 2 adults 1 schoolage
  output$fama2s1 <- renderText({
    if(!is.null(data_of_click$clickedGeography$id)){
      if(nchar(data_of_click$clickedGeography$id)>3){
        puma = puma_per%>%filter(GEOID==data_of_click$clickedGeography$id)
        data = comb_puma_mapinfor %>% filter(PUMA==puma$puma_code & state==puma$states)
        fam <- data%>%filter(fam_type=='a2i0p0s1t0')
        paste0('2 Adults & 1 Schoolage: Median SSS ',prettyNum(fam$median_sss,3,big.mark=","), '/Poverty ',prettyNum(fam$median_poverty,3,big.mark=","))
      }
      else{
        paste0("")}
    }
    else{
      paste0("")}
  })

######################################################
  #obsercevent select state then draw the map.
  observeEvent(list(input$select_state),{

    if (input$select_state == 'No Selection') {
      leafletProxy("main_map")%>%
        flyToBounds(lat1 = 50, lat2 = 30, lng1 = -70, lng2=-130)}

    if (!is.na(input$select_state) &(input$select_state!='No Selection') ) {
      coords <- st_bbox(state_per %>% filter(NAME== input$select_state)) %>% unname
      leafletProxy("main_map") %>%
        flyToBounds(lat1 = coords[2], lat2 = coords[4], lng1 = coords[1], lng2=coords[3])}
    #draw markers
    #if(!is.null(input$select_char)){

    #}
    leafletProxy("main_map",data = update_dataset()) %>%
      clearGroup('Polygon') %>%
      clearGroup('puma') %>%
      addPolygons(fillColor = ~quantcolors()(
                    if(input$select_state == 'No Selection') {per_below_sss}
                    else if(input$select_state != 'No Selection'){per_below_sss_puma}),
                    #else if(input$select_char == 'Neighborhood Advantage'){adi_staternk}),
                  group = "Polygon",
                  fillOpacity = 0.7,
                  color = "grey",
                  weight = 1,
                  layerId = ~GEOID,
                  popup = ~NAME,)%>%
      clearControls() %>%
      addLegend("bottomright",
                pal = quantcolors(),
                values = if(input$select_state == 'No Selection') {~per_below_sss}
                       else if(input$select_state != 'No Selection'){~per_below_sss_puma},
                title = 'SSS Legend',
                group = "Polygon")
    }
  )

  }

shinyApp(ui, server)
