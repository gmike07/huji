import sys


def create_domain_file(domain_file_name, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    domain_file = open(domain_file_name, 'w')  # use domain_file.write(str) to write to domain_file

    s = 'Propositions:\n'
    s += ''.join(f'{sign},{disk},{peg} ' for peg in pegs for disk in disks
                 for sign in ['t', 'f'])
    s += '\n'

    s += 'Actions:\n'
    for peg_start in pegs:
        for peg_end in pegs:
            if peg_start != peg_end:
                for i, disk in enumerate(disks):
                    s += f'Name: {disk},{peg_start},{peg_end}\n'

                    s += f'pre: '
                    s += ''.join(f'f,{disks[j]},{peg_end} ' for j in range(i))
                    s += ''.join(f'f,{disks[j]},{peg_start} ' for j in range(i))
                    s += f't,{disk},{peg_start} f,{disk},{peg_end}\n'

                    s += f'add: f,{disk},{peg_start} t,{disk},{peg_end}\n'
                    s += f'delete: t,{disk},{peg_start} f,{disk},{peg_end}\n'
    domain_file.write(s)

    domain_file.close()


def create_problem_file(problem_file_name_, n_, m_):
    disks = ['d_%s' % i for i in list(range(n_))]  # [d_0,..., d_(n_ - 1)]
    pegs = ['p_%s' % i for i in list(range(m_))]  # [p_0,..., p_(m_ - 1)]
    problem_file = open(problem_file_name_, 'w')  # use problem_file.write(str) to write to problem_file

    s = 'Initial state: '
    s += ''.join(f't,{disk},{pegs[0]} ' for disk in disks)
    s += ''.join(f'f,{disk},{pegs[i]} ' for disk in disks for i in range(1, m_))
    s += '\n'

    s += 'Goal state: '
    s += ''.join(f't,{disk},{pegs[-1]} ' for disk in disks)
    s += ''.join(f'f,{disk},{pegs[i]} ' for disk in disks for i in range(m_-1))
    s += '\n'

    problem_file.write(s)

    problem_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: hanoi.py n m')
        sys.exit(2)

    n = int(float(sys.argv[1]))  # number of disks
    m = int(float(sys.argv[2]))  # number of pegs

    domain_file_name = 'hanoi_%s_%s_domain.txt' % (n, m)
    problem_file_name = 'hanoi_%s_%s_problem.txt' % (n, m)

    create_domain_file(domain_file_name, n, m)
    create_problem_file(problem_file_name, n, m)
