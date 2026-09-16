import Feature26Domain

public enum Feature26DataRepository {
    public static func load(_ id: Int) -> Feature26DomainModel {
        Feature26DomainModel(id: id, title: "Feature 26")
    }
}
