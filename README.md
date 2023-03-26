# Geospatial Data Formatting (Team Map-M8)
## for the Unearthed Sydney 2017 NSW Department of Industry challenge

**[View demo here!](https://atlasmaxima.github.io/unearthedSydney/docs/)**

Atlas, Amanda, Probie, Ming

## Problem

We believe that a considerable amount of the visualisation bottleneck involves
having too many files/file formats, particularly proprietary formats.

## Solution

Establishing a common open file format that can include a wide variety of
geospatial data with associated metadata and allows for faster visualisation.

## Initial implementation

### Tools to convert from existing file formats to normalised coordinate system
Implemented - taking in a CSV of UTM-formatted data to a lat/lon system for
easier integration of large datasets

### File format specification
Open file format specification for implementation across languages and platforms

### Tool for fast querying of large dataset at specific resolution and area
Easy acquisition of relevant subsets from a single file with multiple layers

## Stretch goals/Further steps
Visualisation with an existing engine using fast query tool to limit data
