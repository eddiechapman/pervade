# PERVADE
# Eddie Chapman
# July 19th, 2018

# Load packages
library(dplyr)

# Set directory
setwd("C:/Users/chapman4/PycharmProjects/pervade_nsf_dmps/dmps")

# Load data
# NSF Award data of hits based on keyword filtering
awards <- read.csv('nsf_awards_all.csv', header = T)

code.list <- c('7239', '8083', '8060', '1340', '8020', '027Y', '8018', '8211', '019Y', '8624', '7477', '033Y', '024Y', '8080', '8013', '7495', '7364', '7367', '7719', '041Y', '039Y', '7723', '026Y', '7797', '7796', '7363', '7918', '7726', '8004')

pgm.elem1 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement1Code'))
pgm.elem2 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement2Code'))
pgm.elem3 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement3Code'))
pgm.elem4 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement4Code'))
pgm.elem5 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement5Code'))
pgm.elem6 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement6Code'))
pgm.elem7 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement7Code'))
pgm.elem8 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement8Code'))
pgm.elem9 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement9Code'))
pgm.elem10 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement10Code'))
pgm.elem11 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement11Code')) 
pgm.elem12 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement12Code'))
pgm.elem13 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement13Code'))
pgm.elem14 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement14Code'))
pgm.elem15 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement15Code'))
pgm.elem16 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement16Code'))
pgm.elem17 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement17Code'))
pgm.elem18 <- select(awards, c(AwardIDAwardID, program.element.code = 'ProgramElement18Code'))

pgm.elem <- rbind(pgm.elem1, pgm.elem2, pgm.elem3, pgm.elem4, pgm.elem5, pgm.elem6, pgm.elem7, pgm.elem8, pgm.elem9, pgm.elem10, pgm.elem11, pgm.elem12, pgm.elem13, pgm.elem14, pgm.elem15, pgm.elem16, pgm.elem17, pgm.elem18)

pgm.elem.filtered <- pgm.elem %>%
  mutate(program.element.code = as.character(program.element.code)) %>%
  filter(program.element.code %in% code.list)

awards.filtered <- awards %>%
  inner_join(pgm.elem.filtered)


str(awards.filtered)

write.csv(awards.filtered, 'nsf_awards_cise_parameters.csv')
