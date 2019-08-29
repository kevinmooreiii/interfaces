"""
Test an Arrhenius fit of T, k(T,P) rates to a single Arrhenius function
where the fits are performed using Python
"""

import arrfit


# Obtain list of temperatures and rate constants from initial pair list
PAIRS = [
    ['300', '***'],
    ['400', '***'],
    ['500', '-30.0'],
    ['600', '93.5678'],
    ['700', '2287.02'],
    ['800', '27103.4'],
    ['900', '193348'],
    ['1000', '955781'],
    ['1100', '3.60E+06'],
    ['1200', '1.10E+07'],
    ['1300', '2.85E+07'],
    ['1400', '6.51E+07'],
    ['1500', '1.34E+08'],
    ['1600', '2.52E+08'],
    ['1700', '4.43E+08'],
    ['1800', '7.34E+08'],
    ['1900', '1.16E+09'],
    ['2000', '1.74E+09'],
    ['2100', '2.53E+09'],
    ['2200', '3.56E+09'],
    ['2300', '4.86E+09'],
    ['2400', '6.48E+09'],
    ['2500', '8.45E+09'],
    ['2600', '1.08E+10'],
    ['2700', '1.36E+10'],
    ['2800', '1.68E+10'],
    ['2900', '2.06E+10'],
    ['3000', '2.48E+10']
]
TEMPS = [pair[0] for pair in PAIRS]
RATE_CONSTANTS = [pair[1] for pair in PAIRS]

# Set the T0 value in the (T/T0)^n term in the Arrhenius expr.
T_REF = 1.0


def test__fit():
    """ fit test
    """

    # Print header
    print('\n\nDouble Arrhenius Fit:')

    # Filter the temperatures and rate constants to get valid values
    # k > 0 and k != *** and tmin <= T <= tmax
    tmin = 800
    tmax = 2800
    temps, calc_ks = arrfit.fit.get_valid_temps_rate_constants(
        TEMPS, RATE_CONSTANTS,
        tmin=tmin, tmax=tmax)
    print('Fit Range =', [tmin, tmax])

    # Run a single Arrhenius fit to build a guess for the double fit
    sgl_fit = arrfit.fit.single_arrhenius_fit(
        temps, calc_ks, T_REF)

    # Run a double Arrhenius fit
    fit_params = arrfit.fit.double_arrhenius_fit_scipy(
        sgl_fit[0], sgl_fit[1], sgl_fit[2],
        temps, calc_ks, T_REF)
    print('\nDouble Arrhenius Fit Parameters:')
    print('A1 =', fit_params[0])
    print('n1 =', fit_params[1])
    print('Ea1 =', fit_params[2])
    print('A2 =', fit_params[3])
    print('n2 =', fit_params[4])
    print('Ea2 =', fit_params[5])

    # Calculate fitted rate constants using the fitted parameters
    fit_ks = arrfit.fit.double_arrhenius(
        fit_params[0], fit_params[1], fit_params[2],
        fit_params[3], fit_params[4], fit_params[5],
        T_REF, temps)

    # Print the fitted rate constants and errors
    print('\nComparison of Calculated vs. Fitted Rate Constants:')
    print('Temp (K)  Calc ks      Fit ks')
    for i, _ in enumerate(temps):
        print('{0:6.1f}    {1:1.5E}  {2:1.5E}'.format(
            temps[i], calc_ks[i], fit_ks[i]))

    # Calculate the sum-of-square errors and mean-average-errors
    sse, mean_avg_err, max_avg_err = arrfit.fit.calc_sse_and_mae(
        calc_ks, fit_ks)
    print('\nSSE =', sse)
    print('Mean Avg. Err = ', mean_avg_err)
    print('Max Avg. Err = ', max_avg_err)


if __name__ == '__main__':
    test__fit()