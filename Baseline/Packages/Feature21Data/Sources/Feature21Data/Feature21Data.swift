import Feature21Domain

public enum Feature21DataRepository {
    public static func load(_ id: Int) -> Feature21DomainModel {
        Feature21DomainModel(id: id, title: "Feature 21")
    }
}
