import Feature02Domain

public enum Feature02DataRepository {
    public static func load(_ id: Int) -> Feature02DomainModel {
        Feature02DomainModel(id: id, title: "Feature 2")
    }
}
