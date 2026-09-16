import Feature10Domain

public enum Feature10DataRepository {
    public static func load(_ id: Int) -> Feature10DomainModel {
        Feature10DomainModel(id: id, title: "Feature 10")
    }
}
