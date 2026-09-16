import Feature20Domain

public enum Feature20DataRepository {
    public static func load(_ id: Int) -> Feature20DomainModel {
        Feature20DomainModel(id: id, title: "Feature 20")
    }
}
