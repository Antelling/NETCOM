# NETCOM
Kutztown Networking Chat Application
Authors:         Alan Michener, Anthony Dellinger, Connor Kistler
Creation Date:   11/23/20
Due Date:        11/24/20
Course:          CSC 328
Professor Name:  Dr. Frye
Assignment:      Chat Application
Filename:        README.md
Purpose:         Explain the creation, function and proper use of the chat application including how to build and run, file manifest, responsibility matrix, protocol details,
                 assumptions, and discussion on the development process.
-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------                 
Build:
  The project was coded in python, so there is no need to build the files and there is no required makefile.
Run:  
  Server:
    python3 server.py <port number>
    Note- the server allows for an optional argument to select a specific port number, this argument does not need to be included and will default to 5000 if not
  Client:
    python3 client.py <hostname> <port number>
    Note- the client also allows for the optional port number argument and will default to 5000 if not specified. The hostname hardcoded into the server is localhost currently
File Manifest:
  Lib.py:
    This file contains the library functions for the project that are utilized for both the client and server portions of the project. Lib.py contains functions to create and
    set up the connection objects in both files, to send a message over a connection completely including a message type for handling, and to receive a message from a connection
    and split its composite components.
  server.py:
    This file contains the code for the server portion of the project. User inputs the port number optionally and sets up a connection to listen for client connections on a
    client attempting to connect the server spawns a thread to handle the client, passing the list of established nicknames to allow for nickname verification before 
    listening to receive client messages and logging them to the serverlog file. The server has an exception for a keyboard interrupt to shutdown and close all client connections
    with a CTRL-C interrupt.
  client.py:
    This file contains the code for the client portion of the project. Users input the hostname and optionally a port number to the command-line and are connected to the server
    assuming the server is already up. The user is then prompted for a nickname and will have the nickname verified by the server, needing to re-enter new nicknames until a 
    viable one is verified. After nickname verification the client listens for user input and sends messages across the connection to the server to be logged. If the user inputs
    BYE, the client will send the message to the server to designate client disconnect and the client will close the connection and exit.
  serverlog.txt
    This file contains the log of client connections, messages, and disconnects.
Responsiblility Matrix:
  Connor Kistler:
    Library:
      Connor wrote the library functions for the project and the documentation for the file.
    Client:
      Connor made minor edits to the client to facilitate client exiting.
    Server:
      Connor made edits to the server involving command-line argument handling and minor corrections to logging errors.
    Management:
      Connor was the project manager for the project and coordinated meeting for the group as well as ensuring team members met self imposed project benchmarks. Connor was
      actively involved in the project planning and design process and supplied many ideas that were ultimately used in implementing the project.
  Anthony Dellinger:
    Library:
      Anthony made minor corrections to the library functions to encode and decode messages appropriately.
    Client:
      Anthony made edits to the client to do proper handling of the various message types and help with nickname verification.
    Server:
      Anthony wrote the server file and handled all documentation of the file. Anthony also devised the thread based concurrent processing implementation using the mutex library
    Management:
      Anthony was always present for project meetings and was highly involved in the more intensive planning portions of the project, as well as obviously handling a large 
      majority of the code.
  Alan Michener:
    Client:
      Alan wrote the client file and handled all documentation for the client. Alan also designed the user interface for the project.
    Server:
      Alan suggested the updated logging method for the server as a result of the thread implementation.
    Management:
      Alan was always present for project meetings and was very active in discussion as well as voicing when he had questions to clarify with the group. Alan would often bring
      up concerns in the code that would result in new, more effective methods of implementation after discussion.
Protocol Details:
  HELLO:
    The HELLO protocol message is sent by the client first to the server, and then the server back to the client upon connection. This protocol is used to confirm client-server
    communication before beginning application processes.
  NICK:
    The NICK protocol message is sent by the client to the server containing the user's chosen nickname. The NICK message is used to inform the server that the message contains
    a nickname which needs to be verified and either confirmed or denied back to the client.
  READY:
    The READY protocol message is sent by the server to the client after a valid nickname is sent to the server and verified. The server logs the clients connection when a valid
    username is chosen and sends the READY message to comfirm that the server is ready for user message handling.
  RETRY:
    The RETRY protocol message is sent by the server to the client after an invalid nickname is sent to the server and pinged as already in use. The RETRY message informs the 
    client that the nickname is already in use and that the user must choose a new nickname.
  BYE:
    The BYE protocol message is sent by the client to the server upon client disconnect. The BYE message informs the server that the client has closed their end of the
    connection and that it is okay to close the server end and kill the thread handling that client.
  ERROR:
    The ERROR protocol message is sent by the server to the client whenever the client sends and unexpected message type. The ERROR message was used for testing during the
    implementation of the various other protocol messages and is now simply ignored as it should never occur.
Assumptions:
  The sever has the hostname hard coded into it. For ease of testing the hardcoded username is localhost, meaning the server assumes the server and client are located on the
  same machine. This could easily be changed by simply switching the hostname in the server, but for the purposes of the project it is assumed this way.
  The library functions for the sending and receiving of messages always assume that the CreateConnect() function was called before they are.
Discussion:
  The development process was spotty at times due to our more rushed development cycle. Initially there were a few misunderstandings about the specifications for the project 
  design that needed to be clarified, and took some time to clarify due to a few technical errors. However, after clarifications were made and assured to the group, the 
  process went quite smoothly with various group members picking up the slack of others when necessary in order to meet appropriate benchmarks. An early problem that was 
  encountered was the handling of the server sending messages to the clients after receiving them (which was later clarified to not be part of the specs anymore). That problem
  was solved in theory however, as we realized the client would just need to have a seperate process that is listening for server messages and displaying them to the screen,
  which turned out to be a much simpler solution than expected. Another issue that was encountered was how to share the message data effectively with the master thread for
  logging purposes. This proved to be more difficult as a result of the global mutex and was theorized to be possible by saving the messages to memory and then updating the log
  on client disconnect or server shutdown, however this was obviously inefficient and so the sever was implemented to update the log in the sub-threads.
