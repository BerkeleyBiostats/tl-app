import json
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from core import models

sample_script_inputs = """

{
    "data": {
        "uri": "https://raw.githubusercontent.com/BerkeleyBiostats/tlapp/30821fe37d9fdb2cb645ad2c42f63f1c1644d7c4/cpp.csv",
        "type": "csv",
        "nodes": {
            "Y": "haz",
            "A": "parity",
            "W": ["apgar1", "apgar5", "gagebrth", "mage", "meducyrs", "sexn"]
        }
    },
    "fields": [{
        "name": "Learners",
        "type": "enum",
        "choices": [
            "glmfast",
            "SL.glmnet"
        ]
    }],
    "params": {
        "learners": {
            "glm_learner": {
                "learner": "Lrnr_glm_fast"
            },
            
            "sl_glmnet_learner": {
                "learner": "Lrnr_pkg_SuperLearner",
                "params": {
                    "SL_wrapper":"SL.glmnet"
                }
            }
            
        },
        
        "metalearner": {
            "learner": "Lrnr_nnls"
        }
    }
}

"""

sample_script = """


---
title: "Sample TL App script"
author: "Jeremy Coyle"
date: "9/1/2017"
output: html_document
---

```{r setup, include=FALSE}
library(knitr)
knitr::opts_chunk$set(echo = TRUE)
```

```{r tltools_setup, include=FALSE}
library(tltools)

if(!exists("tlparams")){
  sample_input_file <- fpath <- system.file("extdata", "sample_input.json", package="tltools")
  tlparams <- ScriptParams$new(sample_input_file)
}
```

## Analysis Parameters
```{r comment='', echo=FALSE}
cat(readLines(tlparams$input_file, warn=FALSE), sep = '\n')
```

## Analysis 

```{r analysis, echo=TRUE, cache=T}
# Note for Marc Pare:
# in some sense we might want to separate the part of the script that runs an analysis 
# (computantionally expensive, unlikely to change) from the part of the script that reports the results 
# (runs fast, might change a lot)
# the former would likely be an R script, the latter an Rmd document
# this chunk is the analysis part, the rest is the report part
# just something to think about
library(sl3)
library(SuperLearner)
#define task from tlparams specification
cpp <- tlparams$data
cpp[is.na(cpp)] <- 0
covars <- c(unlist(tlparams$data_nodes$W), tlparams$data_nodes$A)
outcome <- tlparams$data_nodes$Y
task <- sl3_Task$new(cpp, covariates = covars, outcome = outcome)

#define learners based on tlparams
learner_from_params <- function(learner){
  Lrnr_factory <- get(learner$learner)
  params <- learner$params
  
  if(is.null(params)){
    params <- list()
  }
  learner <- do.call(Lrnr_factory$new, params)
  
  return(learner)
}

learners <- lapply(tlparams$params$learners, learner_from_params)
metalearner <- learner_from_params(tlparams$params$metalearner)
sl_learner <- Lrnr_sl$new(learners = learners, metalearner = metalearner)
sl_fit <- sl_learner$train(task)


```

## Results

Just a sample of some output types


### Coef table
```{r coefs, echo=FALSE}
ml_fit <- sl_fit$fit_object$full_fit$fit_object$learner_fits[[2]]$fit_object
coeftab <- as.matrix(coef(ml_fit))
learner_names <- sapply(learners,`[[`,'name')
rownames(coeftab) <- learner_names
colnames(coeftab) <- "Coef"
kable(coeftab)
```

### Coef plot
```{r coef_plot, echo=FALSE, fig.height=2, fig.width=4}
library(ggplot2)
coefdf <- as.data.frame(coeftab)
coefdf$Learner <- learner_names
ggplot(coefdf,aes(y=Learner, x=Coef))+geom_point()+theme_bw()
```

### Coef text
```{r coef_text, echo=FALSE}
print(coeftab)
```

### We can also write output to a file

Nothing to see here

```{r coef_file, echo=FALSE}
csv_file <- file.path(tlparams$output_dir, "coef.csv")
write.csv(coeftab,csv_file)

rdata_file<- file.path(tlparams$output_dir, "coef.rdata")
save(coeftab,file=rdata_file)
```


"""

class Command(BaseCommand):
    help = "Initialize the app for development"

    def handle(self, *args, **options):
        user = User.objects.create_superuser(
            'admin', 'admin@example.com', 'admin')
        user.save()

        parameters = json.loads(sample_script_inputs)

        code = sample_script

        mt = models.ModelTemplate(
            name='sl3_sample.R',
            parameters=parameters,
            code=code
        )   
        mt.save()

        parameters = {
            "fields": [{
                "name": "Spacing",
                "type": "enum",
                "choices": [
                    "tight",
                    "loose",
                ],
            },]
        }

        code = """
            print('foo')
        """

        mt2 = models.ModelTemplate(
            name='Another sample.R',
            parameters=parameters,
            code=code
        )
        mt2.save()

        job = models.ModelRun(
            model_template=mt,
            status=models.ModelRun.status_choices['submitted'],
        )
        job.save()

        job = models.ModelRun(
            model_template=mt2,
            status=models.ModelRun.status_choices['submitted'],
        )
        job.save()

        dataset = models.Dataset(
            title="Subset of growth data from the collaborative perinatal project (CPP)",
            url="https://raw.githubusercontent.com/BerkeleyBiostats/tlapp/30821fe37d9fdb2cb645ad2c42f63f1c1644d7c4/cpp.csv",
            variables={
                "names": [
                    "haz",
                    "parity",
                    "apgar1", 
                    "apgar5", 
                    "gagebrth", 
                    "mage", 
                    "meducyrs", 
                    "sexn"
                ]
            }            
        )
        dataset.save()

        dataset = models.Dataset(
            title="Another sample",
            url="https://raw.githubusercontent.com/BerkeleyBiostats/tlapp/30821fe37d9fdb2cb645ad2c42f63f1c1644d7c4/cpp.csv",
            variables={
                "names": [
                    "foo",
                    "bar",
                ]
            }            
        )
        dataset.save()

