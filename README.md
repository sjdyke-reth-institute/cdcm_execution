# CDCM_reconfig



\documentclass[journal,onecolumn]{IEEEtran}
\usepackage[utf8]{inputenc}
\usepackage{graphicx}






\usepackage{mathrsfs}
\usepackage{amssymb}

\usepackage{amsmath}
\usepackage{epsfig}
\usepackage{color}

\usepackage{hyperref}

\usepackage{systeme}

\documentclass{article}
\usepackage{listings}

\usepackage{xcolor}
\documentclass{article}
\usepackage{amssymb}% http://ctan.org/pkg/amssymb
\usepackage{pifont}% http://ctan.org/pkg/pifont
\newcommand{\cmark}{\ding{51}}%
\newcommand{\xmark}{\ding{55}}%
%New colors defined below
\definecolor{codegreen}{rgb}{0,0.6,0}
\definecolor{codegray}{rgb}{0.5,0.5,0.5}
\definecolor{codepurple}{rgb}{0.58,0,0.82}
\definecolor{backcolour}{rgb}{0.95,0.95,0.92}

%Code listing style named "mystyle"
\lstdefinestyle{mystyle}{
  backgroundcolor=\color{backcolour}, commentstyle=\color{codegreen},
  keywordstyle=\color{magenta},
  numberstyle=\tiny\color{codegray},
  stringstyle=\color{codepurple},
  basicstyle=\ttfamily\footnotesize,
  breakatwhitespace=false,         
  breaklines=true,                 
  captionpos=b,                    
  keepspaces=true,                 
  numbers=left,                    
  numbersep=5pt,                  
  showspaces=false,                
  showstringspaces=false,
  showtabs=false,                  
  tabsize=2
}



\hyphenation{op-tical net-works semi-conduc-tor}


\begin{document}
%

\title{CDCM Design/Architecture Meeting Summary}
%

% \author{\IEEEauthorblockN{Roman Ibrahimov\href{https://orcid.org/0000-0002-9680-7137}{\includegraphics[scale=0.055]{orcid_1.png}} }
        
%   % <-this % stops a space
%   \thanks{Roman Ibrahimov is with the Smart Machine and Assistive Robotics Technology (SMART) Laboratory, Department of Computer and Information Technology, Purdue University, West Lafayette, IN 47907, USA.
%         {\tt\small\{ibrahir@purdue.edu\}}}
% }







% make the title area
\maketitle



\IEEEpeerreviewmaketitle
\textbf{Topics that were covered:}

\underline{dicussed: \textcolor{}{\cmark}, not discussed:} \textcolor{red}{\xmark}
\begin{itemize}
    \item Breaking down into: a) trade studies and b) decision making \textcolor{red}{\xmark}
    \item Code configuration \textcolor{red}{\xmark}
    \item Agent model \textcolor{}{\cmark}
    \item Modularization of the code \textcolor{}{\cmark}
    \item Structure of the code / avoiding dictionaries \textcolor{}{\cmark}
    \item Seperate the system model from the code and test \textcolor{}{\cmark}
    \item Changing the code with easy interface \textcolor{red}{\xmark}
    \item New patch with reconfigured code \textcolor{}{\cmark}
    \item Parallelization \textcolor{}{\cmark}
    \item Adding inventory \textcolor{red}{\xmark}
    \item Activity language \textcolor{red}{\xmark}
    \item Comm. Control/C2 \textcolor{red}{\xmark}
    \item Timestep \textcolor{}{\cmark}
    \item Parameters \textcolor{red}{\xmark}
    
\end{itemize}


\vspace{10mm}



\lstset{style=mystyle}
Here is the example of the system. Data classes in Python are to be used:  
\begin{lstlisting}[language=Python, caption=]

System
    Data: 
        current_state
        inputs = [sys1: ["in1", "in2"],
                  sys2: ["in3", "in4"]]
        next_state 
    
    Methods:
        step(dt)
        transition() (curr_state=next_state)
        
    SolarIrSys:
        current_state = [SolIr]
        next_state 
        step(dt):
            read_from_file
        inputs = None
        transition()
        
    SolarPanelSys:
        current_state = [pacd, power]
        inputs = [solarIr: "solar_ir",
                  dustProc: "dust"]
        step(dt):
            sol = input[...]
            dust = input[...]
            power = f(solar, dust)
            pacd = f(...,...)
        transition()
    SensorPower:
        current_state = [MsPower]
        inputs = SolarPanels.power
        step(dt)
\end{lstlisting}

The following blocks are the examples of defining state with its parameters. 
\begin{lstlisting}[language=Python, caption=]
        
Static Parameter: 
    units (pint)
    description (String)
    value (np.array)
    name
    
State: 
    name
    units
    description
    is.observed
    is.traded
    
    
\end{lstlisting}

% \begin{lstlisting}[language=Python, caption=Python example]

% import numpy as np
    
% def incmatrix(genl1,genl2):
%     m = len(genl1)
%     n = len(genl2)
%     M = None #to become the incidence matrix
%     VT = np.zeros((n*m,1), int)  #dummy variable
    
%     #compute the bitwise xor matrix
%     M1 = bitxormatrix(genl1)
%     M2 = np.triu(bitxormatrix(genl2),1) 

%     for i in range(m-1):
%         for j in range(i+1, m):
%             [r,c] = np.where(M2 == M1[i,j])
%             for k in range(len(r)):
%                 VT[(i)*n + r[k]] = 1;
%                 VT[(i)*n + c[k]] = 1;
%                 VT[(j)*n + r[k]] = 1;
%                 VT[(j)*n + c[k]] = 1;
                
%                 if M is None:
%                     M = np.copy(VT)
%                 else:
%                     M = np.concatenate((M, VT), 1)
                
%                 VT = np.zeros((n*m,1), int)
    
%     return M
% \end{lstlisting}












% The functionality of the Softmax function is the same as the Sigmoid function. However, the Sigmoid is intended for binary-class problems whereas the Softmax is designed for multi-class classification, such as autonomous car recognizing different road signs, pedestrians, road lane, etc. 
% \section{Keras Implementation on the Exercises}

% The first exercise focuses on the implementation of the Keras on famous \textbf{CIDAR-10} dataset that include 60,000 images of size 32 x 32, and of 10 kinds of objects: airplanes, cars, birds, cats, deer, dogs, frogs, horses, ships, and trucks. In the attached \textit{main.py}, the model of Convolutional Neural Network is implemented using Keras. The model consists of a number of hidden layers with a final layer with \textit{Softmax} function that classifies the final results. However, if we pay attention to the accuracy on the test data set, we can easily notice that it fells a way behind the the accuracy on the training set. To avoid all this, we need to tune the hyperparameters. In the attached, \textit{model.py} the techniques that we learned in Chapter 3 are added: 
% \begin{itemize}
%     \item Kaimin He initialization
%     \item Adding $\lamda$ parameter to the cost function 
%     \item Adding dropout layers
% \end{itemize}

% In the final exercise,  \textit{get\_image\_camera.py} the very similar techniques are used using OpenCV platform on the simulated robot. 

% % that's all folks
\end{document}
