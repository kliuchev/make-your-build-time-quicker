import Feature01Domain

public enum Feature01DataRepository {
    public static func load(_ id: Int) -> Feature01DomainModel {
        Feature01DomainModel(id: id, title: "Feature 1")
    }
}
