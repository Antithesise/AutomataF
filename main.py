from AutomataF import atmf

def run(name: str) -> None:
    print(f"\n{name}:")
    with open(name) as f:
        atmf(f.read())

# run("examples/clear.atmf")
# run("examples/clearmsg.atmf")
# run("examples/helloworld.atmf")
# run("examples/quine.atmf")
# run("examples/quine2.atmf")
# run("examples/fibonacci.atmf")
# run("examples/echo.atmf")
# run("examples/multilineecho.atmf")
# run("examples/adder.a185tmf")
# run("examples/subtracter.atmf")
run("examples/doubler.atmf")
# run("examples/truthmachine.atmf")