"""
Pruebas unitarias para el sistema de diagnóstico médico profesional
"""
import unittest
from Diagnostico import diagnostico


class TestDiagnosticoMedico(unittest.TestCase):
    """Clase de pruebas para el módulo de diagnóstico"""

    def test_no_enfermo(self):
        """
        Prueba 1: Paciente saludable (NO ENFERMO)
        
        Parámetros normales:
        - Edad: 25 años (joven)
        - Índice muscular: 28 (bueno)
        - Presión: 110 mmHg (normal)
        - Glucosa: 85 mg/dL (normal)
        - Oxigenación: 98% (excelente)
        - Temperatura: 36.5°C (normal)
        
        Resultado esperado: NO ENFERMO
        """
        resultado = diagnostico(
            edad=25,
            indice_muscular=28,
            presion=110,
            glucosa=85,
            oxigenacion=98,
            temperatura=36.5
        )
        self.assertEqual(resultado, "NO ENFERMO")
        print("✅ Test 1 PASS: Paciente saludable detectado correctamente")

    def test_enfermo_leve(self):
        """
        Prueba 2: Paciente con condición leve (ENFERMO LEVE)
        
        Parámetros con alteraciones leves:
        - Edad: 45 años
        - Índice muscular: 24 (aceptable)
        - Presión: 135 mmHg (hipertensión leve)
        - Glucosa: 110 mg/dL (prediabetes)
        - Oxigenación: 96% (buena)
        - Temperatura: 37.2°C (ligeramente elevada)
        
        Resultado esperado: ENFERMO LEVE
        """
        resultado = diagnostico(
            edad=45,
            indice_muscular=24,
            presion=135,
            glucosa=110,
            oxigenacion=96,
            temperatura=37.2
        )
        self.assertEqual(resultado, "ENFERMO LEVE")
        print("✅ Test 2 PASS: Enfermedad leve detectada correctamente")

    def test_enfermo_agudo(self):
        """
        Prueba 3: Paciente con condición aguda (ENFERMO AGUDO)
        
        Parámetros con alteraciones moderadas:
        - Edad: 55 años
        - Índice muscular: 22 (bajo)
        - Presión: 150 mmHg (hipertensión moderada)
        - Glucosa: 150 mg/dL (hiperglucemia)
        - Oxigenación: 94% (baja)
        - Temperatura: 38°C (fiebre)
        
        Resultado esperado: ENFERMO AGUDO
        """
        resultado = diagnostico(
            edad=55,
            indice_muscular=22,
            presion=150,
            glucosa=150,
            oxigenacion=94,
            temperatura=38
        )
        self.assertEqual(resultado, "ENFERMO AGUDO")
        print("✅ Test 3 PASS: Enfermedad aguda detectada correctamente")

    def test_enfermo_cronico(self):
        """
        Prueba 4: Paciente con condición crónica (ENFERMO CRONICO)
        
        Parámetros con alteraciones graves:
        - Edad: 70 años
        - Índice muscular: 18 (muy bajo - sarcopenia)
        - Presión: 170 mmHg (hipertensión grave)
        - Glucosa: 200 mg/dL (diabetes descontrolada)
        - Oxigenación: 90% (hipoxemia)
        - Temperatura: 39°C (fiebre alta)
        
        Resultado esperado: ENFERMO CRONICO
        """
        resultado = diagnostico(
            edad=70,
            indice_muscular=18,
            presion=170,
            glucosa=200,
            oxigenacion=90,
            temperatura=39
        )
        self.assertEqual(resultado, "ENFERMO CRONICO")
        print("✅ Test 4 PASS: Enfermedad crónica detectada correctamente")

    def test_enfermedad_terminal(self):
        """
        Prueba 5: Paciente en estado crítico (ENFERMEDAD TERMINAL)
        
        Parámetros críticos:
        - Edad: 80 años (edad avanzada)
        - Índice muscular: 15 (desnutrición severa)
        - Presión: 190 mmHg (crisis hipertensiva)
        - Glucosa: 300 mg/dL (hiperglucemia severa)
        - Oxigenación: 85% (hipoxemia grave)
        - Temperatura: 40°C (fiebre muy alta)
        
        Resultado esperado: ENFERMEDAD TERMINAL
        """
        resultado = diagnostico(
            edad=80,
            indice_muscular=15,
            presion=190,
            glucosa=300,
            oxigenacion=85,
            temperatura=40
        )
        self.assertEqual(resultado, "ENFERMEDAD TERMINAL")
        print("✅ Test 5 PASS: Enfermedad terminal detectada correctamente")

    def test_valores_limite_no_enfermo(self):
        """
        Prueba 6: Valores en el límite superior de NO ENFERMO
        
        Verifica que el algoritmo clasifique correctamente
        valores que están justo por debajo del umbral de ENFERMO LEVE
        """
        resultado = diagnostico(
            edad=30,
            indice_muscular=27,
            presion=115,
            glucosa=90,
            oxigenacion=99,
            temperatura=36.6
        )
        self.assertEqual(resultado, "NO ENFERMO")
        print("✅ Test 6 PASS: Valores límite clasificados correctamente")

    def test_valores_limite_enfermo_leve(self):
        """
        Prueba 7: Valores en el límite entre ENFERMO LEVE y ENFERMO AGUDO
        
        Verifica la correcta clasificación en valores límite
        """
        resultado = diagnostico(
            edad=50,
            indice_muscular=23,
            presion=140,
            glucosa=120,
            oxigenacion=95,
            temperatura=37.5
        )
        self.assertIn(resultado, ["ENFERMO LEVE", "ENFERMO AGUDO"])
        print(f"✅ Test 7 PASS: Valor límite clasificado como {resultado}")


class TestValidacionParametros(unittest.TestCase):
    """Pruebas para validar el comportamiento con diferentes parámetros"""

    def test_parametros_normales_multiples_casos(self):
        """
        Prueba 8: Múltiples casos con parámetros normales
        
        Verifica consistencia del algoritmo con diferentes
        combinaciones de parámetros normales
        """
        casos_normales = [
            (20, 30, 115, 90, 99, 36.5),
            (30, 28, 112, 88, 98, 36.6),
            (35, 29, 118, 92, 97, 36.7),
        ]
        
        for caso in casos_normales:
            resultado = diagnostico(*caso)
            self.assertEqual(resultado, "NO ENFERMO",
                           f"Caso {caso} debería ser NO ENFERMO")
        
        print("✅ Test 8 PASS: Múltiples casos normales clasificados correctamente")

    def test_paciente_joven_vs_mayor(self):
        """
        Prueba 9: Comparación paciente joven vs mayor con mismos parámetros
        
        Verifica que la edad influye en el diagnóstico
        """
        # Paciente joven
        resultado_joven = diagnostico(
            edad=25,
            indice_muscular=25,
            presion=130,
            glucosa=100,
            oxigenacion=96,
            temperatura=37
        )
        
        # Paciente mayor con mismos parámetros (excepto edad)
        resultado_mayor = diagnostico(
            edad=75,
            indice_muscular=25,
            presion=130,
            glucosa=100,
            oxigenacion=96,
            temperatura=37
        )
        
        # El paciente mayor debe tener un diagnóstico igual o más grave
        categorias = ["NO ENFERMO", "ENFERMO LEVE", "ENFERMO AGUDO", 
                     "ENFERMO CRONICO", "ENFERMEDAD TERMINAL"]
        
        indice_joven = categorias.index(resultado_joven)
        indice_mayor = categorias.index(resultado_mayor)
        
        self.assertGreaterEqual(indice_mayor, indice_joven,
                               "Paciente mayor debe tener diagnóstico igual o más grave")
        
        print(f"✅ Test 9 PASS: Joven={resultado_joven}, Mayor={resultado_mayor}")

    def test_oxigenacion_critica(self):
        """
        Prueba 10: Impacto de oxigenación crítica
        
        La oxigenación baja debe resultar en diagnóstico grave
        debido a su alta ponderación en el algoritmo
        """
        resultado = diagnostico(
            edad=40,
            indice_muscular=25,
            presion=120,
            glucosa=95,
            oxigenacion=82,  # Oxigenación crítica
            temperatura=36.5
        )
        
        # Con oxigenación crítica, el diagnóstico debe ser al menos AGUDO
        self.assertIn(resultado, ["ENFERMO AGUDO", "ENFERMO CRONICO", "ENFERMEDAD TERMINAL"],
                     "Oxigenación crítica debe resultar en diagnóstico grave")
        
        print(f"✅ Test 10 PASS: Oxigenación crítica detectada - {resultado}")


def run_tests():
    """Función para ejecutar todas las pruebas y mostrar resultados"""
    print("\n" + "="*70)
    print("  EJECUTANDO PRUEBAS UNITARIAS - SISTEMA DE DIAGNÓSTICO MÉDICO")
    print("="*70 + "\n")
    
    # Crear suite de pruebas
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Agregar todas las pruebas
    suite.addTests(loader.loadTestsFromTestCase(TestDiagnosticoMedico))
    suite.addTests(loader.loadTestsFromTestCase(TestValidacionParametros))
    
    # Ejecutar pruebas
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Resumen
    print("\n" + "="*70)
    print("  RESUMEN DE PRUEBAS")
    print("="*70)
    print(f"✅ Pruebas exitosas: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"❌ Pruebas fallidas: {len(result.failures)}")
    print(f"⚠️  Errores: {len(result.errors)}")
    print(f"📊 Total ejecutadas: {result.testsRun}")
    print("="*70 + "\n")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)
