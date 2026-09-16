import Feature33Domain

public enum Feature33DataRepository {
    public static func load(_ id: Int) -> Feature33DomainModel {
        Feature33DomainModel(id: id, title: "Feature 33")
    }
}
