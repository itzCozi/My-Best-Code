import os, sys
import shutil
import subprocess
from datetime import datetime

debug = True


class vars:
  version = '1.0 - First/Last-release'
  user = os.getlogin()
  powershell = str('C:/Windows/System32/powershell.exe')
  web_file = str(f'https://github.com/itzCozi/UPM/blob/main/UPM-source(1.0)/win-version/upm.py')
  scoop_Dir = str(f'C:/Users/{user}/scoop')
  scoopApp_Dir = str(f'{scoop_Dir}/apps/upm')
  scoopShim_File = str(f'{scoop_Dir}/shims/upm.cmd')
  scoopApp_File = str(f'{scoopApp_Dir}/upm.py')
  now = datetime.now().strftime('%Y-%m-%d %H:%M:%S') + '\n\n'

  class upm_files:
    current_Dir = os.getcwd()
    current_repository = 'upm'
    repository = str(f'{current_Dir}/{current_repository}')
    tracked_Dir = str(f'{repository}/tracked_files')
    encoded_Dir = str(f'{repository}/encoded')
    commits = str(f'{repository}/commits')
    builds = str(f'{repository}/builds')
    readme_file = str(f'{repository}/README.md')
    changes_File = str(f'{repository}/changes.txt')


class commands:

  @staticmethod
  def about():
    # Simply prints the version and github
    print('----- Universal Program Manager -----\n')
    print(f'Version: {vars.version}')
    print(f'Current repository: {vars.upm_files.repository}')
    print('Github: https://github.com/itzCozi/UPM')
    return True

  @staticmethod
  def init():
    # Creates and sets up the folder system in current folder that archives changes
    try:
      os.mkdir(vars.upm_files.repository)
      os.mkdir(vars.upm_files.tracked_Dir)
      os.mkdir(vars.upm_files.encoded_Dir)
      os.mkdir(vars.upm_files.commits)
      os.mkdir(vars.upm_files.builds)
      open(vars.upm_files.changes_File, 'w')
      with open(f'{vars.upm_files.changes_File}', 'a') as log:
        log.write(f'{vars.upm_files.current_Dir} | New repository created AT - {vars.now}')
      print(f'{vars.upm_files.current_Dir} | Repository successfully created!')
      return True
    except Exception as e:
      print(f'ERROR: An error occurred, repository not created. \n{e}\n')
      sys.exit(1)

  @staticmethod
  def commit(dir, message):
    # Commit a draft as a folder
    if os.path.exists(dir):
      formatted_msg = message.replace(' ', '-')
      commit_Dir = f'{vars.upm_files.commits}/{formatted_msg}'
      if not os.path.exists(commit_Dir):
        os.mkdir(commit_Dir)
      else:
        print('ERROR: A commit with the same message is already made.')
        sys.exit(1)
    else:
      print('ERROR: Given directory can not be found.')
      sys.exit(1)

    for r, d, f in os.walk(dir):
      for folder in d or f:
        tracked_folder = os.path.join(r, folder)
        new_Dir = str(f'{commit_Dir}/{dir}')
        new_File = str(f'{commit_Dir}/{tracked_folder}')
        if not os.path.exists(new_Dir):
          os.mkdir(new_Dir)
        if not os.path.exists(new_File):
          if os.path.isdir(tracked_folder):
            os.mkdir(new_File)
          else:
            open(new_File, 'w')
      for file in f:
        tracked_path = os.path.join(r, file)
        if not os.path.exists(new_File):
          open(new_File, 'w')
        with open(f'{commit_Dir}/{tracked_path}', 'w') as _file:
          _file.write(open(tracked_path, 'r').read())
      with open(f'{vars.upm_files.changes_File}', 'a') as log:
        log.write(f'{commit_Dir} | New commit has been made AT - {vars.now}')
      print(f'{commit_Dir} | New commit has been made.')
      return True

  @staticmethod
  def track(file):
    # Starts tracking a file's changes
    if os.path.exists(file):
      with open(file, 'r') as Fin:
        file_content = Fin.read()
        file_name = os.path.basename(file).split('/')[-1]
        new_Dir = str(f'{vars.upm_files.tracked_Dir}/{file_name}')
        with open(new_Dir, 'w') as Fout:
          Fout.write(file_content)
      with open(f'{vars.upm_files.changes_File}', 'a') as log:
        log.write(f'{file_name} | New file has tracked AT - {vars.now}')
      print(f'{file_name} | Successfully tracked.')
      return True
    else:
      print('ERROR: File cannot be found.')
      sys.exit(1)

  @staticmethod
  def untrack(file):
    # Just untracks the file
    file_name = os.path.basename(file).split('/')[-1]
    tracked_file = f'{vars.upm_files.tracked_Dir}/{file_name}'
    if os.path.exists(tracked_file):
      try:
        os.remove(tracked_file)
        with open(f'{vars.upm_files.changes_File}', 'a') as log:
          log.write(f'{file_name} | File has been untracked AT - {vars.now}')
        print(f'{file_name} | Has been untracked.')
        return True
      except Exception as e:
        print(f'ERROR: Could not access tracked file. \n{e}\n')
        sys.exit(1)
    else:
      print('ERROR: Given file does not exists.')
      sys.exit(1)

  @staticmethod
  def build(dir, name, version):
    # Creates a folder containing a compiled version of the project
    if os.path.exists(dir):
      formatted_name = name.replace(' ', '-')
      build_Dir = f'{vars.upm_files.builds}/{formatted_name}-{version}'
      if not os.path.exists(build_Dir):
        os.mkdir(build_Dir)
      else:
        print('ERROR: A build with the same message is already made.')
        sys.exit(1)
    else:
      print('ERROR: Given directory can not be found.')
      sys.exit(1)

    for r, d, f in os.walk(dir):
      for folder in d or f:
        tracked_folder = os.path.join(r, folder)
        new_Dir = str(f'{build_Dir}/{dir}')
        new_File = str(f'{build_Dir}/{tracked_folder}')
        if not os.path.exists(new_Dir):
          os.mkdir(new_Dir)
        if not os.path.exists(new_File):
          if os.path.isdir(tracked_folder):
            os.mkdir(new_File)
          else:
            open(new_File, 'w')
      for file in f:
        tracked_path = os.path.join(r, file)
        if not os.path.exists(new_File):
          open(new_File, 'w')
        with open(f'{build_Dir}/{tracked_path}', 'w') as _file:
          _file.write(open(tracked_path, 'r').read())
      with open(f'{vars.upm_files.changes_File}', 'a') as log:
        log.write(f'{build_Dir} | New build has been created AT - {vars.now}')
      print(f'{build_Dir} | New build has been created.')
      return True

  @staticmethod
  def update(file):
    # Updates the saved file with the given file
    file_name = os.path.basename(file).split('/')[-1]
    if os.path.exists(f'{vars.upm_files.tracked_Dir}/{file_name}'):
      try:
        with open(file, 'r') as Fout:
          file_content = Fout.read()
          with open(f'{vars.upm_files.tracked_Dir}/{file_name}', 'w') as Fin:
            Fin.write(str(file_content))
          with open(f'{vars.upm_files.changes_File}', 'a') as log:
            log.write(f'{file_name} | Tracked file has been updated AT - {vars.now}')
          print(f'{file_name} | Saved file has been updated.')
          return True
      except Exception as e:
        print(f'ERROR: Could not access files, Maybe try as admin. \n{e}\n')
        sys.exit(1)
    else:
      print('ERROR: Given file is not being tracked.')
      sys.exit(1)

  @staticmethod
  def change_repo(repo):
    # Change current working repository
    dummy_repo = str(f'{vars.upm_files.current_Dir}/{repo}')
    if os.path.exists(dummy_repo):
      vars.upm_files.current_repository = str(repo)
      with open(f'{vars.upm_files.changes_File}', 'a') as log:
        log.write(f'{repo} | Working repository has been changed AT - {vars.now}')
      print(f'{repo} | Working repository has been changed.')
    else:
      print('ERROR: Given repository doesnt exist in current directory')
      sys.exit(1)

  @staticmethod
  def clear_changes():
    # Clears the changes file
    try:
      if os.path.exists(vars.upm_files.changes_File):
        with open(f'{vars.upm_files.changes_File}', 'a') as file:
          file.truncate(0)
          file.write(f'Changes file cleared! AT - {vars.now}')
          file.close()
        print('Changes file has been cleared.')
    except Exception as e:
      print(f'ERROR: Could not access changes file. \n{e}\n')
      sys.exit(1)

  @staticmethod
  def add_readme():
    # Add a readme.md to your current repo
    if not os.path.exists(vars.upm_files.repository):
      print('ERROR: There is no repository detected.')
      sys.exit(1)
    if os.path.exists(vars.upm_files.readme_file):
      print('ERROR: File already exists in repository')
      sys.exit(1)

    try:
      with open(vars.upm_files.readme_file, 'w') as file:
        file.write('Please edit this `README.md` made by upm.')
        file.close()
      with open(f'{vars.upm_files.changes_File}', 'a') as log:
        log.write(f'{vars.upm_files.readme_file} | README.md file created - AT {vars.now}')
      print(f'{vars.upm_files.readme_file} | README.md file created.')
    except Exception as e:
      print(f'ERROR: Could not create new file \n{e}\n')
      sys.exit(1)

  @staticmethod
  def scoop_setup():
    # Setup the scoop app
    if not os.path.exists(vars.scoopApp_Dir):
      try:
        driver.scoopSetup()
        print('Scoop app setup use `upm` to call to it.')
      except Exception as e:
        print(f'ERROR: Could not setup scoop app. \n{e}\n')
        sys.exit(1)
    else:
      print('ERROR: The scoop `upm` app is already detected.')
      sys.exit(1)

  @staticmethod
  def uninit(repo):
    # Deletes the repository
    try:
      for dir in os.listdir(vars.upm_files.current_Dir):
        if dir == str(repo):
          shutil.rmtree(dir)
          with open(f'{vars.upm_files.changes_File}', 'a') as log:
            log.write(f'Repository {dir} has been deleted AT - {vars.now}')
          print(f'Repository {dir} has been deleted.')
          break
        else:
          pass
    except Exception as e:
      print(f'ERROR: Could not access needed files. \n{e}\n')
      sys.exit(1)

  @staticmethod
  def zip_repo(name):
    # Zip the current repository named after the input
    zip_location = f'{vars.upm_files.current_Dir}/{name}'
    zip_obj = shutil.make_archive(zip_location, 'zip', vars.upm_files.repository)

    if os.path.exists(zip_location):
      print('Zip already created.')
    else:
      zip_obj
      with open(f'{vars.upm_files.changes_File}', 'a') as log:
        log.write(f'Zip named {name} created AT - {vars.now}')
      print(f'Zip called {name} created.')

  @staticmethod
  def filter_file(file, word):
    # Search a file for given word and remove it
    if not os.path.exists(file):
      print(f"ERROR: Given file {file} cannot be found.")
      sys.exit(1)
    try:
      with open(file, "r+") as Fin:
        content = Fin.read()
      if word in content:
        with open(file, "w+") as Fout:
          write_item = content.replace(word, "")
          Fout.write(write_item)
      else:
        print(f"ERROR: {word} cannot be found in {file}.")
        sys.exit(1)
    except Exception as e:
      print(f'ERROR: An unkown error occured when running command. \n{e}\n')
      sys.exit(1)


class driver:

  @staticmethod
  def scoopSetup():
    # Setup program files and dependencies
    if os.path.exists(vars.scoop_Dir):
      if debug:
        print('Scoop is already installed. ')
      pass
    else:
      subprocess.call(f'{vars.powershell} iwr -useb get.scoop.sh | iex')
      print('We have installed scoop for you this is so you can use \
        \nour program with calling to it with `python upm.py` \
        \ninstead try and use `upm` to call to the program.')

    if os.path.exists(vars.scoop_Dir):
      if not os.path.exists(vars.scoopApp_Dir):
        os.mkdir(vars.scoopApp_Dir)

      if not os.path.exists(vars.scoopShim_File):
        with open(vars.scoopShim_File, 'w') as file:
          file.write(f'@"{vars.scoopApp_File}" %*')
      if debug:
        print(f'Program file {vars.scoopShim_File} !MISSING!')

      if not os.path.exists(vars.scoopApp_File):
        with open(__file__, 'r') as Fout:
          file_content = Fout.read()
        with open(vars.scoopApp_File, 'w') as Fin:
          Fin.write(file_content)
        if debug:
          print(f'Program file {vars.scoopApp_File} !MISSING!')
    else:
      pass

  @staticmethod
  def mercyHelper():
    # This creates a file called HELP.txt with helpful info
    if os.path.exists(vars.upm_files.repository):
      new_file = f'{vars.upm_files.repository}/HELP.txt'
    else:
      new_file = f'{vars.upm_files.current_Dir}/HELP.txt'
    if not os.path.exists(new_file):
      open(new_file, 'x')
    with open(new_file, 'w') as file:
      file.write('Github:https://github.com/itzCozi/UPM\n')
      file.write('Wiki: https://github.com/itzCozi/UPM/wiki\n')
      file.write('''
Commands | Description
init : Creates `upm` folder and repository
about : Displays relative context
commit : Create a new commit with given name
track : Starts saving given file
untrack : Removes given save file
update : Update the given tracked file
build : Create a new build and store it in repository
clear_changes : Wipes the changes file
uninit : Deletes detected repository
change_repo : Changes working repository
scoop_setup : Sets up scoop console app
zip_repo : Zips the current repository and names it
add_readme : Adds a `README.md` file to the repository
filter_file : Looks for given word in file and removes it
      ''')
      file.close()

  @staticmethod
  def argHandler():
    if sys.argv[1] == 'init':
      commands.init()
    elif sys.argv[1] == 'about':
      commands.about()
    elif sys.argv[1] == 'clear_changes':
      commands.clear_changes()
    elif sys.argv[1] == 'scoop_setup':
      commands.scoop_setup()
    elif sys.argv[1] == 'add_readme':
      commands.add_readme()
    elif sys.argv[1] == 'uninit':
      try:
        commands.uninit(sys.argv[2])
      except Exception as e:
        print(f"Please provide proper parameters : uninit 'upm' \n{e}\n")
    elif sys.argv[1] == 'commit':
      try:
        commands.commit(sys.argv[2], sys.argv[3])
      except IndexError:
        print("Please provide proper parameters : commit 'C:/project/source' Bug Fix #69")
    elif sys.argv[1] == 'track':
      try:
        commands.track(sys.argv[2])
      except Exception as e:
        print(f"Please provide proper parameters : track 'C:/project/users.txt' \n{e}\n")
    elif sys.argv[1] == 'untrack':
      try:
        commands.untrack(sys.argv[2])
      except Exception as e:
        print(f"Please provide proper parameters : untrack 'test/lol.py' \n{e}\n")
    elif sys.argv[1] == 'change_repo':
      try:
        commands.change_repo(sys.argv[2])
      except Exception as e:
        print(f"Please provide proper parameters : change_repo 'Extra' \n{e}\n")
    elif sys.argv[1] == 'update':
      try:
        commands.update(sys.argv[2])
      except Exception as e:
        print(f"Please provide proper parameters : update 'C:/test.txt' \n{e}\n")
    elif sys.argv[1] == 'build':
      try:
        commands.build(sys.argv[2], sys.argv[3], sys.argv[4])
      except Exception as e:
        print(f"Please provide proper parameters : build 'C:/upm.txt' TESTBUILD 1.0.0 \n{e}\n")
    elif sys.argv[1] == 'zip_repo':
      try:
        commands.zip_repo(sys.argv[2])
      except Exception as e:
        print(f"Please provide proper parameters : zip_repo 'C:/upm' Obama-Coding16 \n{e}\n")
    elif sys.argv[1] == 'filter_file':
      try:
        commands.filter_file(sys.argv[2], sys.argv[3])
      except Exception as e:
        print(f"Please provide proper parameters : filter_file 'C:/test.txt' 'pizza' \n{e}\n")

    else:
      print("To use upm you must pass valid arguments via the command-line such as: \
        \npython upm.py track 'happy-420/snoop.cpp'")

if __name__ == '__main__':
  try:
    driver.argHandler()
  except IndexError:
    driver.mercyHelper()
    print('ERROR: No arguments passed.')
    sys.exit(1)
  except Exception as e:
    print(f'CRIT-ERROR: A unknown runtime-error occurred. \n{e}\n')
    driver.mercyHelper()
    sys.exit(1)
else:
  print('You cannot use upm as a import instead \
    \ndrag it into your project directory and pass \
    \narguments using the console or terminal in VSCode.')
  sys.exit(1)
