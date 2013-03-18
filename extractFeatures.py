#!/usr/bin/python
# Author : Rajat Khanduja
# 
# Extracts features from the files in the directory.
#
# Usage :-
#   python extractFeatures.py <directory_path>
#
# Features extracted (in the order they will be printed)
# 1. Drug1 (in the pair)
# 2. Drug2 (in the pair)
# 3. Head word of drug1
# 4. Head word of drug2


import os
import xml.etree.ElementTree as ET
import nltk


def extractFeaturesForPair(pairRef, sentenceRef, entity1Ref, entity2Ref):
  '''
  Function that extracts features for every pair given the entities involved
  and the parent sentence and returns it as a dictionary
  '''
  
  features = {}
  sentence = sentenceRef.attrib['text']

  # Get names of drugs.
  features['drug1'] = entity1Ref.attrib['text']
  features['drug2'] = entity2Ref.attrib['text']

  # Head words of the drugs.
  features['head1'] = features['drug1'].split()[0]
  features['head2'] = features['drug2'].split()[0]

  # Distance between drug names (ignoring stopwords)
  limitsDrug1 = map (lambda x: x.split("-"), entity1Ref.attrib['charOffset'].split(";"))
  limitsDrug2 = map (lambda x: x.split("-"), entity2Ref.attrib['charOffset'].split(';'))
  if int(limitsDrug1[-1][1]) < int(limitsDrug2[0][0]):
    textBetweenDrugs = sentence[int(limitsDrug1[-1][1]) + 1: int(limitsDrug2[0][0])].strip()  

  else:
    textBetweenDrugs = ""
  wordsBetweenDrugs = len(filter(lambda x: 
                            x not in nltk.corpus.stopwords.words('english'),
                              textBetweenDrugs.split()))
  features['distanceBetweenDrugs'] = wordsBetweenDrugs

  # Relation exists or not
  features['ddi'] = pairRef.attrib['ddi']
  

  return features

  
def processFile(filename):
  root = ET.parse(filename).getroot()
  features = dict()
  for sentence in root:
    entities = []
    for child in sentence:
      if child.tag == "entity":
        entities.append(child)
      if child.tag == "pair":
        entity1 = filter(lambda x: x.attrib['id'] == child.attrib['e1'], 
                          entities)[0]

        entity2 = filter(lambda x: x.attrib['id'] == child.attrib['e2'], 
                          entities)[0]
        
        features[child.attrib['id']] = extractFeaturesForPair(child, sentence, 
                                                              entity1, entity2)
  return features                                                              

def processDir (directory):
  features = dict()
  for (path, dirs, files) in os.walk(directory):
    for f in files:
      features.update(processFile(os.path.join(path, f)))
  return features

if __name__ == "__main__":
  import sys
  directory = sys.argv[1]
  features = processDir(directory)
  delimiter = ",;,"
  for pair in features:
    entry = pair 
    entry += delimiter + features[pair]['drug1']
    entry += delimiter + features[pair]['drug2']
    entry += delimiter + features[pair]['head1']
    entry += delimiter + features[pair]['head2']
    entry += delimiter + str(features[pair]['distanceBetweenDrugs'])
    entry += delimiter + features[pair]['ddi']
    print entry
