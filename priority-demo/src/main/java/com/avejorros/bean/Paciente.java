package com.avejorros.bean;

public class Paciente implements Comparable<Paciente> {
  private String nombre;
  private String sintoma;
  private char codigoEmergencia; // A (más urgente) a E (menos urgente)

  public Paciente(String nombre, String sintoma, char codigoEmergencia) {
    this.nombre = nombre;
    this.sintoma = sintoma;
    this.codigoEmergencia = codigoEmergencia;
  }

  @Override
  public int compareTo(Paciente otro) {
    return Character.compare(this.codigoEmergencia, otro.codigoEmergencia);
  }

  public String getNombre() {
    return nombre;
  }

  public void setNombre(String nombre) {
    this.nombre = nombre;
  }

  public String getSintoma() {
    return sintoma;
  }

  public void setSintoma(String sintoma) {
    this.sintoma = sintoma;
  }

  public char getCodigoEmergencia() {
    return codigoEmergencia;
  }

  public void setCodigoEmergencia(char codigoEmergencia) {
    this.codigoEmergencia = codigoEmergencia;
  }

  @Override
  public String toString() {
    return nombre + ", " + sintoma + ", " + codigoEmergencia;
  }
}
