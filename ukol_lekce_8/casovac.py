from math import fabs

class Casovac:
    def rozdil_tiku(posledni_cas_ns: int, cas_ted_ns: int):
        return fabs(cas_ted_ns - posledni_cas_ns)/1000000000.0
    
    # vraci True pokud cas mezi dvemi vstupnimi argumenty je vetsi nez pozadovany interval
    # jinak vraci False
    def ubehl_cas(posledni_cas_ns, cas_ted_ns, interval_s):
        rozdil_s = Casovac.rozdil_tiku(posledni_cas_ns, cas_ted_ns)
        return rozdil_s > interval_s