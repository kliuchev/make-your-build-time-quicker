import Feature08Domain

public enum Feature08DataRepository {
    public static func load(_ id: Int) -> Feature08DomainModel {
        Feature08DomainModel(id: id, title: "Feature 8")
    }
}
