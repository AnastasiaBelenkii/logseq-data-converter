**KINDA BROKEN-- STILL IN DEVELOPMENT-- USE AT OWN RISK-- THIS CODE IS VERY BAD-- NO TESTS ANYWHERE**

## Intro and Rationale

This is a quick python script that will convert logseq-formatted markdown blocks to various formats-- namely gnu rec and (output-only for now) csv. You can actually use logseq as a kinda sort plain-text database, but in order to get any solid use out of it, you have to write datalog queries within the context of the application and rely on logseq to actually display the query results for you. This is actually not bad, but misses out on the [substantial ecosystem](https://github.com/dbohdan/structured-text-tools/blob/master/README.md) of excellent tools to work with small-scale data stored in plain text, and locks you into logseq to make your data usable. Most of that ecosystem works off of csv and json, so those are the priority formats I'm trying to target. Especially CSV. I started with gnu rec because it's reasonably close in syntax (at least visually) to using logseq-style properties under blocks with a one-block-per-record style, and it seemed like a good backup/export format from logseq's markdown-- even if the target destination of the backup doesn't have this script (which already has a csv output target), you can always use rec2csv and then go nuts with tools like miller or visidata on top of all the standard POSIX utilities. Personally, I find rec also a little bit nicer for ongoing/semi-random-one-at-a-time data entry than something like JSON or CSV. Recutils on its own is also quite nice for one-off tasks. However, after I clean up this small MVP I likely will not have a continuing focus on gnu rec over the more widely used formats. 

## Install and Usage

The procedure below is far from ideal, but it's how I'm currently using the script myself. I recommend not using this until I have a proper working module on pip somewhere

1. git clone to {install_dir}
2. `chmod +x main.py` and `chmod +x lsqdata.sh`
3. `sudo update-alternatives --install /usr/local/bin/lsqdata lsqdata {install_dir}/lsqdata.sh 50`
  - make sure to use a full absolute path for {install_dir}

Or just copy the sh file somewhere into the path.

## Things you can use this for

note: this is in the context of having slowly reformatted a lot of my life to operate off of plaintext, but here is a oneliner I was just able to run to show me all emails from any instutions that are likely to want money from me, from within the last week:

```bash
for name in $(lsqdata accounts.md csv | mlr --csv --headerless-csv-output uniq -g Institution); do notmuch search "from:$name date:1w"; done
```

Not even a script. a single command. I don't even have to maintain a separate csv file-- literally just convert on demand a handwritten note that I can also create live queries and views within logseq for. [Miller](https://miller.readthedocs.io/en/latest/) is also amazing, go check them out

[Just going to drop this here as well](https://github.com/hauntsaninja/pyp)

## limitations

- handle multi-word fieldnames(rec)/property names(markdown)-- since IIRC logseq doesn't allow property names to have spaces
- no CSV input
- no multiline text in rec or LSQ-markdown, not even sure how to translate that to csv yet
- no record set identifiers in rec or page identifiers/nested blocks in LSQ markdown
- not even an actual module and using it on own machine using terrible shell script
- rec to csv is broken
    - not sure how much this matters given that rec2csv exists but FYI

## longer term plans

- at least some type of testing lol
- JSON I/O
- YAML, TOML I/O
- addressing some of the limitations above-- CSV input, multiline text fields, better handling of markdown features in conversions, nested blocks in LSQ markdown
- mass converting files matching some pattern between formats
- someday: scraping blocks containing properties out of mostly-text markdown files and centralizing them in a different format in their own location

## final notes

this was all likely incoherent and I apologize lol. it is late here
