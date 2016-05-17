import sys
import os
import re

vttfn = 'lecture2.en.vtt' # sys.argv[1]
srtfn = 'lecture2.en.srt' # sys.argv[2]

def extractCue(line):
    cuetagp = re.compile('::cue\((.+\..+?)\)')
    try:
        return re.search(cuetagp,line).group(1)
    except:
        return None

def removeFixedPatterns(line):
    p1 = re.compile('align:.+?%')
    # can add more patterns here
    line = p1.sub('', line)
    return line

def removeTags(line, cuetags):
    for tag in cuetags:
        head,tail = tag.split('.')
        startTag = '<' + tag + '>'
        implicitTag = '<' + head + '>'
        endTag = '</' + head + '>'
        line = line.replace(startTag,'')
        line = line.replace(endTag,'')
        line = line.replace(implicitTag,'')
    return line

def removeTimeAngleTag(line):
    p = re.compile('<(\d\d:\d\d:\d\d.+?)>')
    return p.sub('',line)

testFlag = False

if testFlag:
    cuetags = ['c.colorE5E5E5','c.colorCCCCCC']
    # test extractCue
    #extractCue('::cue(c.colorCCCCCC) { color: rgb(204,204,204);')

    # test removeFixedPatterns
    #print removeFixedPatterns('00:00:00.000 --> 00:00:02.590 align:start position:0%')
    #print removeFixedPatterns('<c.colorE5E5E5>welcome</c><00:00:00.859><c> to</c><c.colorE5E5E5><00:00:00.969><c> lecture</c></c><00:00:01.339><c> to</c><c.colorE5E5E5><00:00:01.530><c>')

    # test removeTimeAngleTag
    #print removeTimeAngleTag('<c.colorE5E5E5>well<00:40:31.130><c> and</c></c><00:40:32.250><c> then</c><c.colorE5E5E5><00:40:32.430><c> the</c></c><00:40:32.760><c> most</c><00:40:33.020><c> recent</c>')
    #print removeTimeAngleTag('<c.colorCCCCCC>2007 had a journal</c><c.colorE5E5E5> version</c><c.colorCCCCCC> think</c>')
    line1 = '<c.colorE5E5E5>well<00:40:31.130><c> and</c></c><00:40:32.250><c> then</c><c.colorE5E5E5><00:40:32.430><c> the</c></c><00:40:32.760><c> most</c><00:40:33.020><c> recent</c>'
    line1 = removeTags(line1, cuetags)
    line1 = removeTimeAngleTag(line1)
    print line1
else:
    with open(vttfn) as vttf, open(srtfn,'w') as srtf:
    	startFlag = False
        subtitleCNT = 1
        cuetags = []
        srtText = ''
    	for line in vttf:
            line = line.strip() + ' '
            if line=='': continue
            if '##' in line: startFlag = True
            # generate cuetags
            if not startFlag:
                tag = extractCue(line)
                if tag: cuetags.append(tag)
                continue
            # removeFixedPatterns: such as align, you can add more
            line = removeFixedPatterns(line)
            line = removeTags(line, cuetags)
            line = removeTimeAngleTag(line)
            if '-->' in line:
                srtText += '\n\n' + str(subtitleCNT) + '\n' + line + '\n'
                subtitleCNT += 1
            else:
                srtText += line
        srtText = srtText.replace('.',',')
        srtf.write(srtText + '\n')
        srtf.flush()
