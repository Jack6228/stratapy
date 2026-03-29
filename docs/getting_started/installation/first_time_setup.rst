First Time Setup
============================================

.. note::
   If you are new to Python or programming, and these concepts are unfamiliar to you, remember that online alternatives which require no installation are available, such as Google Colab. See the `Using Online Platforms <online_platforms.html>`__ guide for more details.

Stratapy uses the Python programming language, so you will need to have Python installed on your computer before you can use stratapy. The panel below provides step-by-step instructions on how to install Python, depending on your operating system (Windows, MacOS, Linux). Follow the instructions carefully to set up your Python environment.

.. tab-set::

    .. tab-item:: Windows

        On Windows, you can install Python either through the Windows Store or by downloading it directly from the official Python website.

        To use the Windows Store:

        1. Open the Microsoft Store app on your computer.

        2. Search for "Python" in the search bar.

        3. Select the latest version of Python (e.g., Python 3.13) from the search results.

        4. Click the "Get" or "Install" button to download and install Python.

        To download from the official website:

        1. Go to the official Python website: `https://www.python.org/downloads/windows/ <https://www.python.org/downloads/windows/>`_

        2. Click on the latest Python version for Windows to download the installer.    

        3. Run the downloaded installer. Make sure to check the box that says "Add Python to PATH" before clicking "Install Now".

        4. Follow the prompts to complete the installation.

    .. tab-item:: MacOS

        On MacOS, you can install Python using the Homebrew package manager or by downloading it directly from the official Python website.

        To use Homebrew:

        1. Open the Terminal application on your Mac.

        2. If you don't have Homebrew installed, you can install it by running the following command:

           ``/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"``

        3. Once Homebrew is installed, run the following command to install Python:

           ``brew install python``

        To download from the official website:

        1. Go to the official Python website: `https://www.python.org/downloads/macos/ <https://www.python.org/downloads/macos/>`_

        2. Click on the latest Python version for MacOS to download the installer.

        3. Run the downloaded installer and follow the prompts to complete the installation.

    .. tab-item:: Linux

        On Linux, you can install Python using your distribution's package manager.

        For Debian-based distributions (like Ubuntu):

        1. Open the Terminal application.

        2. Run the following command to update your package list:

           ``sudo apt update``

        3. Install Python by running:

           ``sudo apt install python3``

        For Red Hat-based distributions (like Fedora):

        1. Open the Terminal application.

        2. Run the following command to install Python:

           ``sudo dnf install python3``

        For Arch Linux:

        1. Open the Terminal application.

        2. Run the following command to install Python:

           ``sudo pacman -S python``

Once you have installed Python, you can verify the installation by opening a terminal or command prompt and typing:
    
.. code-block:: bash

   python --version

This should display the version of Python that you have installed. You are now ready to proceed with installing stratapy and its dependencies.

.. tip::

   Instead of running Python code through the terminal, you can also use an Integrated Development Environment (IDE) for a more user-friendly experience. For beginners, we recommend using `Visual Studio Code (VS Code) <https://code.visualstudio.com/>`_, developed by Microsoft. For example, it enables the use of Jupyter Notebooks, which are interactive coding environments that allow you to write and execute code in a more visual way. This documentation includes examples using Jupyter Notebooks, which can be run directly within VS Code.
   
   Instructions for installing VS Code can be found on their website at `https://code.visualstudio.com/docs/setup/setup-overview <https://code.visualstudio.com/docs/setup/setup-overview>`_.