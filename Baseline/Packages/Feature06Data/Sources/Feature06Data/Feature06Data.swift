import Feature06Domain

public enum Feature06DataRepository {
    public static func load(_ id: Int) -> Feature06DomainModel {
        Feature06DomainModel(id: id, title: "Feature 6")
    }
}
