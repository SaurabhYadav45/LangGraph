# ********************* LONG TERM MEMORY *********************

# It allows sytem to store information across different conversations or session.
# It stores the behaviour of user across diff conversations to give a personalized response to each user.
# It is stored in stores.
# It stores the facts, concept & experience  in the form of json
# Long-term memories are stored in custom namespaces.

# What is a Namespace?
# Think of a namespace as a folder or directory.
# For example,

# Store

# ├── Rahul
# │      Memory 1
# │      Memory 2
# │      Memory 3
# │
# ├── Alice
# │      Memory 1
# │      Memory 2
# │
# └── Bob
#        Memory 1

# There are 3 types of Long term memory

# 1. Semantic Memory : PERSONALIZATION
    # It stores facts and concept learnt from previous interactions to personalized the application
    # It is your general knowledge about the world.
    # Paris is the capital of France.

    # Example:
    # Python is a programming language.
    # Water freezes at 0°C.
    # A dog is a mammal.

    # I'm a backend engineer
    # I likes consize explanation

    # {
    #     "profession": "Backend Engineer",
    #     "response_style":"concise"
    # }

    # Now when you asked your ai to explain kubernentes, it'll give you consize explanation rather than long explanation.

    # How it is stored :
    # {
    #     "name": "Rahul",
    #     "profession": "Backend Engineer",
    #     "language": "Python",
    #     "response_style": "Concise",
    #     "timezone": "IST"
    # }

    # Two approach to design Semantic Memory:
        # 1. Single Profile
        # 2. collection of several documents


# 2. Episodic Memory : It stores the previous experiences

    # Example-1: Medical Assistant

    # Semantic:
    # Patient is diabetic.
    # Allergic to penicillin.

    # Episodic:
    # Last consultation
    # ↓
    # Complained about headaches
    # ↓
    # Blood pressure measured
    # ↓
    # Medication adjusted
    # ↓
    # Symptoms improved


    # Example-2 : Customer Support

    # Semantic Memory:
    # Customer has Premium Plan.
    # Customer lives in Germany.
    # Preferred language is English.

    # Episodic Memory:
    # Last refund request
    # ↓
    # Verified purchase
    # ↓
    # Escalated to billing
    # ↓
    # Refund processed


# 3. Procedural Memory: It stores knowledge about how to perform certain tasks.

    # It is a procedure for solving a class of tasks.
    # It emphasis on How should I respond?

    # For example:
    # When writing code:

    # 1. Explain the approach
    # 2. Write the code
    # 3. Explain edge cases
    # 4. Mention time complexity

    # For AI Agents the Procedural memory is encoded in the Agent's System Prompt.

    # Suppose your system prompt says:

    # You are a helpful coding assistant.
    # Always
    # - Explain before coding
    # - Use Python unless asked otherwise
    # - Mention complexity
    # - Be concise


    # Example:
    # Imagine you're building an AI tutor.
    # Procedural memory might be

    # When answering
    # ↓
    # Start with intuition
    # ↓
    # Give formal definition
    # ↓
    # Provide example
    # ↓
    # Ask a follow-up question
