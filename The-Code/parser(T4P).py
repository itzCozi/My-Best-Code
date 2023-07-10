### This file really stumped me so there's a lot of documentation. ###
# Used to parse the question set file to create a usable list for the GUI.
import os, sys
import random
import string


class files:
  base_dir = f'C:/Users/{os.getlogin()}/test4py'
  set_file = f'{base_dir}/set.txt'
  log_file = f'{base_dir}/logs.txt'
  sesh_file = f'{base_dir}/session.txt'


class set:
  # // - Exculdes the whole line
  # :: - Begin a new question
  # ;; - End current question
  # ?? - Writen before the question
  # [] - Embed a file in the question
  # ! - Symbolize incorrect answer
  # * - Correct answer choice
  # __ - Begin answer choice section

  def parseSet(file):
    # Makes the question set into a list
    if not os.path.exists(file):
      print(f'ERROR: Could not find {file}.')
      sys.exit(1)

    with open(file, 'r') as f:
      content = f.read()
      fcontent = content.splitlines()
      f.close()

    alphabet = string.ascii_uppercase
    questions = []
    retlist = []

    for Qline in fcontent:
      # Exclude comment lines from question-scout
      if '::' in Qline and '//' not in Qline:
        qStart = fcontent.index(Qline)
        fcontent.remove(Qline)
      if ';;' in Qline and '//' not in Qline:
        qEnd = fcontent.index(Qline)
        fcontent.remove(Qline)

        questionOBJ = fcontent[qStart:qEnd]
        if questionOBJ not in questions:
          questions.append(questionOBJ)

    for item in questions:  # For every question in the list
      ticker = -1          # Counts up to 26 for each letter
      allAnswers = []      # All of the answers
      parsed_answers = []  # The answers with a letter infront
      embedded = None      # If the question has an embed
      for line in item:  # For each newline in the choosen question
        # Index: Returns the index of the item in a given list
        # Find: Returns index of the word in a string/line
        if '??' in line:
          questionIndex = line.find('??')
          question = line[questionIndex:].replace('??', '')
        if '__' in line:
          aStart = item.index(line)
        if '[' and ']' in line:
          embedded = True
          embedStart = line.find('[')
          embedEnd = line.find(']')
          embedded_path = line[embedStart:embedEnd] + ']'

      for Aline in item[aStart:]:  # For every line after the __ symbol
        if '//' in Aline or Aline == '':
          pass  # Ignore comment lines/blank lines
        elif '!' == Aline[0]:
          allAnswers.append(Aline.replace('!', ''))
        elif '*' == Aline[0]:
          # We dont replace the asterisk because we need to idetify the correct
          # answer later on in GUI.py we will replace it before outputting answer choices
          allAnswers.append(Aline)

      for ans in allAnswers:  # Assign a uppercase letter to each choice A.
        ticker += 1
        if ticker <= 26:  # Max 26 answer choices due to alphabet length
          letter = list(alphabet)[ticker]
        else:
          ticker = -1  # Reset the count if ticker greater than 26
        answer_choice = f'{letter}. {ans}'
        parsed_answers.append(answer_choice)

      split_answers = '\n'.join(parsed_answers)  # Cannot use \n in f-strings
      if embedded == True:  # If there is an embed in this question
        embedded_path = embedded_path.replace('[', '').replace(']', '')
        with open(embedded_path, 'r') as ef:
          embedded_content = ef.read()
          ef.close()
        parsed_question = f'{question} \
        \n{embedded_content} \
        \n{split_answers}'

      else:  # If there is not an embed
        parsed_question = f'{question} \
        \n{split_answers}'

      retlist.append(parsed_question.replace('  ', ''))
    return retlist

  def searchList(INlist, target):
    # Searches a list for a character or sequence
    if not isinstance(INlist, list):
      print('ERROR: INlist must be a list type variable.')
      sys.exit(1)

    for item in INlist:
      if target in item:
        index = INlist.index(item)
        return int(index)

  def writeSet(set):
    # Writes given variable to file
    with open(files.set_file, 'wb') as out:
      out.write(set)
      out.close()

  def jumbleSet(set):
    # Shuffles the question set
    randnum = random.randint(2, 4)
    for i in range(randnum):
      random.shuffle(set)
    return set


def createSet():
  # Creates complete question set and returns it (self-explanitory)
  package = []
  if os.path.getsize(files.set_file) == 0:
    raise Exception('Set file is empty.')
  for question in set.parseSet(files.set_file):
    qlist = question.splitlines()
    ans_index = int(set.searchList(qlist, 'A. '))
    prompt = qlist[0]

    embedded = qlist[1:ans_index]
    answer_choices = qlist[ans_index:]
    embedded = '\n'.join(embedded)

    bundle = [prompt, embedded, answer_choices]
    package.append(bundle)
  return set.jumbleSet(package)
