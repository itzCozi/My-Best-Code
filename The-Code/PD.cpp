// This is old code i am more experinced now

// MADE FOR WINDOWS SYSTEMS
#include <direct.h> //For making folders on windows
#include <filesystem>
#include <fstream>
#include <iostream>
#include <stdlib.h>
#include <string>
#include <unistd.h>
// Creating directorys in linux
/*
#include <bits/stdc++.h>
#include <sys/stat.h>
#include <sys/types.h>
*/

// Global variables
const std::string menuOpts = 
  "1. Read database \n"
  "2. Record to database \n"
  "3. Encryption & Decryption \n"
  "4. Wipe the database \n"
  "5. Exit \n\n";
const char *filePathPTR = "D:/Big Project Coding/Personal-Database/compiled/data/database.db";

// CRYPTOGRAHPY
class encdec 
{
  int key;

  // File name to be encrypt
  std::string file = filePathPTR;
  char c;

public:
  void encrypt();
  void decrypt();
};

// Definition of encryption function
void encdec::encrypt() 
{
  // Key to be used for encryption
  std::cout << "key: ";
  std::cin >> key;

  // Input stream
  std::fstream fin, fout;

  // Open input file
  fin.open(file, std::fstream::in);
  fout.open("encrypted_database.txt", std::fstream::out);

  // Reading original file till end of file
  while (fin >> std::noskipws >> c)
  {
    int temp = (c + key);

    // Write temp as char in output file
    fout << (char)temp;
  }

  // Closing both files
  fin.close();
  fout.close();
}

// Definition of decryption function
void encdec::decrypt()
{
  std::cout << "key: ";
  std::cin >> key;
  std::fstream fin;
  std::fstream fout;
  fin.open("encrypted_database.txt", std::fstream::in);
  fout.open("decrypted_database.txt", std::fstream::out);

  while (fin >> std::noskipws >> c)
  {
    // Remove the key from the character
    int temp = (c - key);
    fout << (char)temp;
  }

  fin.close();
  fout.close();
}

// Functions
void Protocol_wipeData()
{
  std::ofstream filePathPTR("filename.txt");              // Without append
  std::ofstream clearFile("filename.txt", std::ios::app); // with append
}

void Protocol_setup()
{
  // Is ran at the beggining of all menu options to verify the file and folder is setup
  struct stat sb;

  if (mkdir("D:/Big Project Coding/Personal-Database/compiled/data", 0777) == -1) {
    mkdir("D:", 0777);
    mkdir("D:/Big Project Coding", 0777);
    mkdir("D:/Big Project Coding/Personal-Database", 0777);
    mkdir("D:/Big Project Coding/Personal-Database/compiled", 0777);
    mkdir("D:/Big Project Coding/Personal-Database/compiled/data", 0777);

    std::cout << "Directory created \n";
  }

  if (stat(filePathPTR, &sb) == 0 && !(sb.st_mode & S_IFDIR))
  {
    std::cout << "Database is vaild \n";
  }

  else
  {
    std::ofstream Creatingdatabase(filePathPTR);
    std::cout << "Database created \n";
  }
}

void Protocol_wipe()
{
  std::ofstream ofs;
  ofs.open(filePathPTR, std::ofstream::out | std::ofstream::trunc);
  ofs.close();
}

// Main
int main()
{
  // Class variables
  int menuChoice;
  std::string folderPath = "D:/Big Project Coding/Personal-Database/compiled/data";
  std::string filePath = "D:/Big Project Coding/Personal-Database/compiled/data/database.db";

  system("clear");
  std::cout << "              __________ Personal Database __________          "
               "    \n\n\n";
  std::cout << menuOpts;
  std::cout << "> ";
  std::cin >> menuChoice;

  if (menuChoice == 1)
  {
    std::string quitText;
    std::string containedText;

    Protocol_setup();
    system("clear");

    // Open file
    std::ifstream Database(filePath);

    while (getline(Database, containedText))
    {
      // Output the text from the file
      std::cout << containedText << "\n";
    }

    std::cout << "\n\n ---- Quit to exit ---- \n";
    std::cin >> quitText;
    sleep(1); // Try system("pause"); if this no work
    Database.close();
    main();
  }

  if (menuChoice == 2)
  {
    int x = -1;
    int lineAmount;
    std::string quitText;
    std::string userRecord;
    std::string containedText;

    Protocol_setup();
    system("clear");

    std::cout << "Number of lines: ";
    std::cin >> lineAmount;

    system("clear");

    // Creates an instance of ofstream and opens database
    std::ofstream Database_write(filePath, std::ios::app);

    while (x < lineAmount)
    {
      getline(std::cin, userRecord);
      // Outputs to database
      Database_write << userRecord << "\n";

      x++;

      // Closes file after user inputs max times
      if (x == lineAmount)
      {
        Database_write.close();

        system("clear");
        std::cout << "---- Reading Database ----\n\n";

        // Opens for reading the file
        std::ifstream Database_read(filePath);

        while (getline(Database_read, containedText))
        {
          // Output the text from the file
          std::cout << containedText << "\n";
        }

        sleep(2);
        std::cout << "\n\n ---- Quit to exit ---- \n";
        std::cin >> quitText;
        // system("pause") for windows
        sleep(1);
        Database_read.close();
        main();
      }
    }
  }

  if (menuChoice == 3)
  {
    encdec enc;
    int ED_choice;

    Protocol_setup();
    system("clear");

    std::cout << "---- Encryption & Decryption ----\n\n";
    std::cout << "1. Encrypt database\n";
    std::cout << "2. Decrypt database\n\n";

    std::cout << ": ";
    std::cin >> ED_choice;

    if (ED_choice == 1)
    {
      system("clear");

      enc.encrypt();

      std::cout << "Encrypted\n";
      sleep(2);
      main();
    }
    if (ED_choice == 2)
    {
      system("clear");

      enc.decrypt();

      std::cout << "Decrypted\n";
      sleep(2);
      main();
    } 
    else
    {
      std::cout << "Invaild Input\n";
      sleep(2);
      main();
    }
  }

  if (menuChoice == 4)
  {
    char y;
    char n;
    char yORn;
    std::string quitConfirm;

    Protocol_setup();
    system("clear");

    std::cout << "Are you sure you want to wipe the database and the encrypted "
                 "databases in the folder? (y/n) ";
    std::cin >> yORn;

    if (yORn == y)
    {
      Protocol_wipe();

      std::cout << "Wiped!\n";
      sleep(2);
      main();
    }

    if (yORn == n)
    {
      Protocol_wipe();

      std::cout << "Cancled returning to main menu\n";

      sleep(2);
      main();
    }

    else
    {
      std::cout << "Invaild input\n";
      sleep(2);
      main();
    }
  }

  if (menuChoice == 5)
  {
    return 0;
  }

  else
  {
    std::cout << "Invaild input\n";
    sleep(2);
    main();
  }
}