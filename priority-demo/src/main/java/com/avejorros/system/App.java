package com.avejorros.system;

import java.io.BufferedReader;
import java.io.FileReader;
import java.util.Scanner;

import com.avejorros.bean.Paciente;
import com.avejorros.controller.VectorHeap;

/**
 * Hello world!
 * @author mogue - 
 */
public class App {
    private static VectorHeap<Paciente> priority = new VectorHeap<>();
    private static Scanner sc = new Scanner(System.in);

    public static void main(String[] args) {
        cargarPacientesIniciales("src/main/java/com/avejorros/resources/data.txt");
        boolean flag = true;
        while (flag) {
            System.out.println("\n | ----- [Sistema de Emergencias] ----- |");
            System.out.println("1. Agregar paciente manualmente");
            System.out.println("2. Mostrar próximo paciente a atender");
            System.out.println("3. Atender próximo paciente");
            System.out.println("4. Salir");
            System.out.print("Seleccione una opción: ");

            int opcion = sc.nextInt();
            sc.nextLine(); 

            switch (opcion) {
                case 1:
                    agregarPacienteManual();
                    break;
                case 2:
                    mostrarProximoPaciente();
                    break;
                case 3:
                    atenderPaciente();
                    break;
                case 4:
                    System.out.println("Saliendo del sistema...");
                    flag = false;
                default:
                    System.out.println("Opción inválida.");
            }
        }
    }

    public static void agregarPacienteManual() {
        System.out.print("Nombre del paciente: ");
        String nombre = sc.nextLine();
        System.out.print("Síntoma: ");
        String sintoma = sc.nextLine();
        System.out.print("Código de emergencia (A-E): ");
        char codigo = sc.nextLine().toUpperCase().charAt(0);

        if (codigo < 'A' || codigo > 'E') {
            System.out.println("Código inválido. Debe ser A, B, C, D o E.");
            return;
        }

        priority.add(new Paciente(nombre, sintoma, codigo));
        System.out.println("Paciente agregado correctamente.");
    }

    public static void mostrarProximoPaciente() {
        if (priority.isEmpty()) {
            System.out.println("No hay pacientes en espera.");
            return;
        }
        Paciente proximo = priority.getFirst(); 
        System.out.println("Próximo paciente a atender:");
        System.out.println(proximo);
    }

    public static void atenderPaciente() {
        if (priority.isEmpty()) {
            System.out.println("No hay pacientes para atender.");
            return;
        }
        Paciente atendido = priority.remove();
        System.out.println("Paciente atendido:");
        System.out.println(atendido);
    }

    public static void cargarPacientesIniciales(String filePath) {
        try (BufferedReader br = new BufferedReader(new FileReader(filePath))) {
            String line;
            while ((line = br.readLine()) != null) {
                String[] datos = line.split(", ");
                priority.add(new Paciente(datos[0], datos[1], datos[2].charAt(0)));
            }
            System.out.println("Pacientes iniciales cargados desde archivo.");
        } catch (Exception e) {
            System.out.println("Error al cargar pacientes iniciales: " + e.getMessage());
        }
    }
}
