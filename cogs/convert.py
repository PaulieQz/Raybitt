@commands.command()
async def convert(self, ctx, value: float, unit_from, unit_to):
    # Map alternate unit names to their standard forms
    alternate_units = {
        'oz': 'o',
        'gm': 'g',
        'gram': 'g',
        'inches': 'in',
        'cm': 'in',
        'celsius': 'c',
        'fahrenheit': 'f',
        'miles': 'mi',
        'kilometers': 'km',
        'feet': 'ft',
        'meters': 'm',
        'liters': 'l',
        'gallons': 'gal',
        'milliliters': 'ml',
        'fluidounces': 'fl_oz',
        'minutes': 'min',
        'seconds': 'sec',
        'hours': 'hr',
        'squarefeet': 'sq_ft',
        'squaremeters': 'sq_m',
    }
    
    unit_from = alternate_units.get(unit_from.lower(), unit_from.lower())
    unit_to = alternate_units.get(unit_to.lower(), unit_to.lower())

    conversions = {
        'cm_to_in': value * 0.393701,
        'in_to_cm': value * 2.54,
        'c_to_f': (value * 9 / 5) + 32,
        'f_to_c': (value - 32) * 5 / 9,
        'g_to_o': (value * 0.035274),
        'o_to_g': (value * 28.3495),
        'mi_to_km': value * 1.60934,
        'km_to_mi': value / 1.60934,
        'ft_to_m': value * 0.3048,
        'm_to_ft': value / 0.3048,
        'lb_to_kg': value * 0.453592,
        'kg_to_lb': value / 0.453592,
        'l_to_gal': value * 0.264172,
        'gal_to_l': value / 0.264172,
        'ml_to_fl_oz': value * 0.033814,
        'fl_oz_to_ml': value / 0.033814,
        'min_to_sec': value * 60,
        'sec_to_min': value / 60,
        'hr_to_min': value * 60,
        'min_to_hr': value / 60,
        'sq_ft_to_sq_m': value * 0.092903,
        'sq_m_to_sq_ft': value / 0.092903,
        'mph_to_kph': value * 1.60934,
        'kph_to_mph': value / 1.60934
    }

    conversion_key = f"{unit_from}_to_{unit_to}"
    if conversion_key in conversions:
        converted_value = conversions[conversion_key]
        await ctx.send(f"{value} {unit_from} is equal to {converted_value} {unit_to}")
    else:
        await ctx.send("Invalid conversion!")
