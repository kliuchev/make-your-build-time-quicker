import Feature18Domain

public enum Feature18DataRepository {
    public static func load(_ id: Int) -> Feature18DomainModel {
        Feature18DomainModel(id: id, title: "Feature 18")
    }
}
