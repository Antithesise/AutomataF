def atmf(program: str) -> None:
    program: list[str] = list(program)

    if not program: # exit if program is empty
        return

    def inc(text: list[str], index: int) -> list[str]: # increment chr
        text[index] = chr((ord(text[index]) + 1) % 1114112)
        return text

    def dec(text: list[str], index: int) -> list[str]: # decrement chr
        text[index] = chr((ord(text[index]) - 1) % 1114112)
        return text

    def sqr(text: list[str], index: int) -> list[str]: # square chr
        text[index] = chr((ord(text[index]) ** 2) % 1114112)
        return text

    pointer: int = 0
    reset = True

    while True:
        skip = False
        c = False
        j = False

        sindex = {}
        jname = ""

        loopn = 0

        lineno = 0
        index = -1

        if reset:
            pointer = 0
        else:
            reset = True

        lines = {k:len("".join(program).split("\n")[k])+1 for k in range(len("".join(program).split("\n")))}
        lines.update({-1:-1})

        oldprogram = program

        while True:
            if index + 1 >= len(oldprogram):
                break

            index += 1

            instruction = oldprogram[index]

            if index in sindex: # if instruction is to be skipped
                if sindex[index] > 0:
                    sindex[index] += 1

                    continue

            if instruction == "\n":
                lineno += 1
            
            elif instruction == "#": # toggle comment
                c = not c
            elif c: # if currently parsing comment or file name
                continue

            elif instruction == "~": # jump to another file
                if j:
                    try:
                        with open(jname, "r") as f:
                            atmf(f.read())
                    except OSError:
                        pass # FileNotFoundError

                j = not j
            elif j:
                jname += instruction

                if index + 1 == len(oldprogram):
                    try:
                        with open(jname, "r") as f:
                            atmf(f.read())
                    except OSError:
                        pass # FileNotFoundError

            elif skip: # skip to next iteration
                index = len(oldprogram)

            elif instruction == ",": # clear screen
                print(end="\u001b[2J\u001b[1000A\r")

            elif instruction == "<": # decrement pointer
                pointer -= 1
            elif instruction == ">": # increment pointer
                pointer += 1
            elif instruction == "{": # decrement pointer by 10
                pointer -= 10
            elif instruction == "}": # increment pointer by 10
                pointer += 10
            elif instruction == "$": # move pointer to start of line
                pointer = lines[lineno-1] + 1
            elif instruction == "@": # move pointer to end of line
                pointer = lines[lineno]

            elif instruction == "?": # don't reset pointer next iteration
                reset = not reset

            elif instruction == "%": # jump execution to pointer
                index = pointer - 1
            elif instruction == "^" and pointer != index: # skip next chracter if pointer doesn't point this chracter
                index += 1

            elif instruction == "[": # start loop
                loops = index

                loopn = 1
            elif instruction == "]": # end loop
                if program[pointer] == chr(0) or loopn == ord(program[loops-1]): # exit loop if cell at pointer is 0 or loop has completed
                    loopn = 1
                else:
                    index = loops

                    loopn += 1

            elif pointer == len(oldprogram): # if index error is to be expected
                return print()

            elif instruction == ":" or ord(oldprogram[pointer]) < 0 or ord(oldprogram[pointer]) == 1114111: # set cell to 0 at pointer
                program[pointer] = chr(0)
            elif instruction == "-": # decrement cell at pointer
                program = dec(program, pointer)
            elif instruction in "+": # increment cell at pointer
                program = inc(program, pointer)
            elif instruction == ")": # decrement cell at pointer by 10
                for _ in range(10):
                    program = dec(program, pointer)
            elif instruction in "(": # increment cell at pointer by 10
                for _ in range(10):
                    program = inc(program, pointer)
            elif instruction in "*": # square cell at pointer
                program = sqr(program, pointer)

            elif instruction == ".": # halt
                return print()

            elif instruction in ";": # print ASCII of cell at pointer
                if pointer < len("".join(program).rstrip(".!$@")):
                    print(end=program[pointer], flush=True)
            elif instruction in "_": # print cell at pointer
                if pointer < len("".join(program).rstrip(".!$@")):
                    print(end=str(ord(program[pointer])), flush=True)

            elif instruction == "!": # skip to next iteration unless pointer points to a ".", "!", "$", or "@" or if it is at the end
                skip = True

                if program[pointer] in ".!$@": # if the character at the pointer is a ".", "!", "$", or "@"
                    return print()
                elif pointer - 1 == len(program): # if the pointer is at the end of the file
                    skip = False

                    continue
            
            elif instruction == "|": # set cell at pointer to user input
                program[pointer] = input("> ")[0]
            elif instruction == "`": # set cell at pointer to ASCII chr of user input
                program[pointer] = chr(int(input("> ")) % 1114112)
