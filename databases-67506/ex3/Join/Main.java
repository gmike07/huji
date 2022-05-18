package Join;

public class Main {

	/**
	 * @param args
	 */
	public static void main(String[] args) {
		if (args.length != 4 && args.length != 5 && args.length != 6) {
			System.out.println("Wrong number of arguments");
			System.out.println("For part A: exercise_part "
					+ "input_file output_file temp_path");
			System.out.println("For part B: exercise_part "
					+ "input_file1 input_file2 output_file"
					+ " temp_path");
			System.out.println("For part C: exercise_part "
					+ "input_file1 input_file2 output_file"
					+" substrSelect temp_path");
			System.out.println("For part D: exercise_part "
					+ "input_file1 input_file2 output_file"
					+" substrSelect temp_path");
			System.exit(1);
		}

		String exercisePart = args[0];
		

		IExternalMemory e = new ExternalMemoryImpl();

		if (exercisePart.equals("A") || exercisePart.equals("a")) {
			String in = args[1];
			String out = args[2];
			String tmpPath = args[3];
			e.sort(in, out, tmpPath);

		} else if (exercisePart.equals("B") || exercisePart.equals("b")){
			String in1 = args[1];
			String in2 = args[2];
			String out = args[3];
			String tmpPath = args[4];
			e.sortAndJoin(in1,in2, out, tmpPath);

		}
		else if (exercisePart.equals("C") || exercisePart.equals("c")){
			String in1 = args[1];
			String in2 = args[2];
			String out = args[3];
			String substrSelect=args[4];
			String tmpPath = args[5];
			e.joinAndSelect(in1, in2, out, substrSelect, tmpPath);
		}
		else if (exercisePart.equals("D") || exercisePart.equals("d")){
			String in1 = args[1];
			String in2 = args[2];
			String out = args[3];
			String substrSelect=args[4];
			String tmpPath = args[5];
			e.joinAndSelectEfficiently(in1, in2, out, substrSelect, tmpPath);
		}	

		else
			System.out.println("Wrong usage: first argument"
					+ "should be a, b, c OR d only!");

	}

}
