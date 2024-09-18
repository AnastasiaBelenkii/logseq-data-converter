**KINDA BROKEN-- STILL IN DEVELOPMENT-- USE AT OWN RISK-- THIS CODE IS VERY BAD**

## Intro and Rationale

This is a quick python script that will convert logseq-formatted markdown blocks to various formats-- namely gnu rec and (output-only for now) csv. You can actually use logseq as a kinda sort plain-text database, but in order to get any solid use out of it, you have to write datalog queries within the context of the application and rely on logseq to actually display the query results for you. This is actually not bad, but misses out on the [substantial ecosystem](https://github.com/dbohdan/structured-text-tools/blob/master/README.md) of excellent tools to work with small-scale data stored in plain text, and locks you into logseq to make your data usable. Most of that ecosystem works off of csv and json, so those are the priority formats I'm trying to target. Especially CSV. I started with gnu rec because it's reasonably close in syntax (at least visually) to using logseq-style properties under blocks with a one-block-per-record style, and it seemed like a good backup/export format from logseq's markdown-- even if the target destination of the backup doesn't have this script (which already has a csv output target), you can always use rec2csv and then go nuts with tools like miller or visidata on top of all the standard POSIX utilities. Personally, I find rec also a little bit nicer for ongoing/semi-random-one-at-a-time data entry than something like JSON or CSV. Recutils on its own is also quite nice for one-off tasks. However, after I clean up this small MVP I likely will not have a continuing focus on gnu rec over the more widely used formats. 

## Install and Usage

TBD-- don't use this yet lol

## limitations

- no CSV input
- no multiline text in rec or LSQ-markdown, not even sure how to translate that to csv yet
- no record set identifiers in rec or page identifiers/nested blocks in LSQ markdown
- all input formats need a newline at the end of the input or they won't be parsed
   - for now, possibly forever??
    - https://github.com/lark-parser/lark/discussions/1041 ):
- not even an actual module and using it on own machine using terrible shell script
- rec to csv is broken
    - not sure how much this matters given that rec2csv exists but FYI

## longer term plans

- JSON I/O
- YAML, TOML I/O
- addressing some of the limitations above-- CSV input, multiline text fields, better handling of markdown features in conversions, nested blocks in LSQ markdown
- mass converting files matching some pattern between formats
- someday: scraping blocks containing properties out of mostly-text markdown files and centralizing them in a different format in their own location

## final notes

this was all likely incoherent and I apologize lol. it is late here
