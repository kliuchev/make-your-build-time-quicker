import Feature07Domain

public enum Feature07DataRepository {
    public static func load(_ id: Int) -> Feature07DomainModel {
        Feature07DomainModel(id: id, title: "Feature 7")
    }
}
