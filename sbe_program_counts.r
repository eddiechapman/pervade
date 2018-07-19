# PERVADE
# Eddie Chapman
# July 19th, 2018

# Load packages
library(dplyr)
library(readr)

# Set directory
setwd("C:/Users/chapman4/Downloads/PERVADE")

# Load data
# NSF Award data of hits based on keyword filtering
awards <- read.csv('nsf_award_statistics.csv', header = T)

# List of filenames made as subset of above data set. Directorate = SBE & false positives removed. 
relevant.cse.awards <- read.csv('relevant_cse_awards.txt', header = F, col.names = c('Filename'))

# Keep only SBE directorate results, match with list of relevant awards. 
sbe <- awards %>%
  filter(Directorate == 'Direct For Social, Behav & Economic Scie') %>%
  inner_join(relevant.cse.awards, by = c('Filename'))

# Many program columns are repeated in each row (program 1, program 2 etc.).
# This creates a new data frame for each repetition so they can later be merged.
# Trying to count each reference regardless of the orginial column it came from (row is important).
pgm.elem1 <- select(sbe, c(Award.ID, program.element.code = 'Program.Element.1.Code', program.element.text = 'Program.Element.1.Text'))
pgm.elem2 <- select(sbe, c(Award.ID, program.element.code = 'Program.Element.2.Code', program.element.text = 'Program.Element.2.Text'))
pgm.elem3 <- select(sbe, c(Award.ID, program.element.code = 'Program.Element.3.Code', program.element.text = 'Program.Element.3.Text'))
pgm.elem4 <- select(sbe, c(Award.ID, program.element.code = 'Program.Element.4.Code', program.element.text = 'Program.Element.4.Text'))
pgm.elem5 <- select(sbe, c(Award.ID, program.element.code = 'Program.Element.5.Code', program.element.text = 'Program.Element.5.Text'))
pgm.elem6 <- select(sbe, c(Award.ID, program.element.code = 'Program.Element.6.Code', program.element.text = 'Program.Element.6.Text'))
pgm.elem7 <- select(sbe, c(Award.ID, program.element.code = 'Program.Element.7.Code', program.element.text = 'Program.Element.7.Text'))
pgm.elem8 <- select(sbe, c(Award.ID, program.element.code = 'Program.Element.8.Code', program.element.text = 'Program.Element.8.Text'))
pgm.elem9 <- select(sbe, c(Award.ID, program.element.code = 'Program.Element.9.Code', program.element.text = 'Program.Element.9.Text'))

pgm.ref1 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.1.Code', program.Reference.text = 'Program.Reference.1.Text'))
pgm.ref2 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.2.Code', program.Reference.text = 'Program.Reference.2.Text'))
pgm.ref3 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.3.Code', program.Reference.text = 'Program.Reference.3.Text'))
pgm.ref4 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.4.Code', program.Reference.text = 'Program.Reference.4.Text'))
pgm.ref5 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.5.Code', program.Reference.text = 'Program.Reference.5.Text'))
pgm.ref6 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.6.Code', program.Reference.text = 'Program.Reference.6.Text'))
pgm.ref7 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.7.Code', program.Reference.text = 'Program.Reference.7.Text'))
pgm.ref8 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.8.Code', program.Reference.text = 'Program.Reference.8.Text'))
pgm.ref9 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.9.Code', program.Reference.text = 'Program.Reference.9.Text'))
pgm.ref10 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.10.Code', program.Reference.text = 'Program.Reference.10.Text'))
pgm.ref11 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.11.Code', program.Reference.text = 'Program.Reference.11.Text'))
pgm.ref12 <- select(sbe, c(Award.ID, program.Reference.code = 'Program.Reference.12.Code', program.Reference.text = 'Program.Reference.12.Text'))

# Packing them back into a big tall list.
pgm.elem <- rbind(pgm.elem1, pgm.elem2, pgm.elem3, pgm.elem4, pgm.elem5, pgm.elem6, pgm.elem7, pgm.elem8, pgm.elem9)
pgm.ref <- rbind(pgm.ref1, pgm.ref2, pgm.ref3, pgm.ref4, pgm.ref5, pgm.ref6, pgm.ref7, pgm.ref8, pgm.ref9, pgm.ref10, pgm.ref11, pgm.ref12)

# Totalling the number of program references.
pgm.elem.count <- pgm.elem %>%
  count(program.element.code, sort = TRUE)

# Totalling the number of program references.
pgm.ref.count <- pgm.ref %>%
  count(program.Reference.code, sort = TRUE)

# Display top programs referenced in set. 
head(pgm.elem.count, n = 20)
head(pgm.ref.count, n = 20)
